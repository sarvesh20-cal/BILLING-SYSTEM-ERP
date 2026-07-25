import mysql.connector
import bcrypt


class AuthSystem:

    def __init__(self):

        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            port=3306,
            database="billing_system"
        )

        self.cursor = self.connection.cursor()

        print("Database Connected Successfully")


    # ==========================================================
    # LOGIN USER
    # ==========================================================

    def login_user(self, username, password):

        try:

            # --------------------------------------------------
            # GET USER
            # --------------------------------------------------

            query = """
                SELECT
                    user_id,
                    full_name,
                    username,
                    password,
                    role,
                    failed_attempts,
                    is_locked
                FROM users
                WHERE username = %s
            """

            self.cursor.execute(query, (username,))
            user = self.cursor.fetchone()

            # --------------------------------------------------
            # USER NOT FOUND
            # --------------------------------------------------

            if not user:

                return {
                    "status": False,
                    "message": "User Not Found"
                }

            user_id = user[0]
            full_name = user[1]
            db_username = user[2]
            stored_password = user[3]
            role = user[4]

            # Handle NULL values safely
            failed_attempts = user[5] if user[5] is not None else 0
            is_locked = user[6] if user[6] is not None else 0


            # --------------------------------------------------
            # CHECK ACCOUNT LOCK
            # --------------------------------------------------

            if is_locked:

                return {
                    "status": False,
                    "message": "Account Locked. Contact Administrator."
                }


            # --------------------------------------------------
            # PASSWORD VERIFICATION
            # Supports bcrypt AND old plain-text passwords
            # --------------------------------------------------

            match = False

            try:

                # If password is bcrypt encrypted
                if stored_password.startswith("$2"):

                    match = bcrypt.checkpw(
                        password.encode("utf-8"),
                        stored_password.encode("utf-8")
                    )

                else:

                    # Old/plain-text password
                    match = password == stored_password

            except Exception as password_error:

                print("Password Check Error:", password_error)

                # Fallback for old passwords
                match = password == stored_password


            # ==================================================
            # LOGIN SUCCESS
            # ==================================================

            if match:

                # Reset failed attempts
                self.cursor.execute(
                    """
                    UPDATE users
                    SET failed_attempts = 0
                    WHERE user_id = %s
                    """,
                    (user_id,)
                )

                self.connection.commit()

                print("LOGIN SUCCESS")

                return {
                    "status": True,
                    "user_id": user_id,
                    "full_name": full_name,
                    "username": db_username,
                    "role": role
                }


            # ==================================================
            # WRONG PASSWORD
            # ==================================================

            else:

                failed_attempts = failed_attempts + 1

                self.cursor.execute(
                    """
                    UPDATE users
                    SET failed_attempts = %s
                    WHERE user_id = %s
                    """,
                    (failed_attempts, user_id)
                )

                self.connection.commit()


                # --------------------------------------------------
                # LOCK AFTER 5 FAILED ATTEMPTS
                # --------------------------------------------------

                if failed_attempts >= 5:

                    self.cursor.execute(
                        """
                        UPDATE users
                        SET is_locked = 1
                        WHERE user_id = %s
                        """,
                        (user_id,)
                    )

                    self.connection.commit()

                    return {
                        "status": False,
                        "message": "Account Locked After 5 Failed Attempts"
                    }


                return {
                    "status": False,
                    "message":
                        f"Incorrect Password ({failed_attempts}/5)"
                }


        except mysql.connector.Error as err:

            print("DATABASE ERROR:", err)

            return {
                "status": False,
                "message": f"Database Error: {err}"
            }


        except Exception as err:

            print("ERROR:", err)

            return {
                "status": False,
                "message": str(err)
            }


    # ==========================================================
    # CLOSE DATABASE CONNECTION
    # ==========================================================

    def close_connection(self):

        try:

            if self.cursor:
                self.cursor.close()

            if self.connection:
                self.connection.close()

        except Exception as e:

            print("Connection Close Error:", e)