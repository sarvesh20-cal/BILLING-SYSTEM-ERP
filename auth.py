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

        # DEBUG
        self.cursor.execute("SELECT @@port")
        print("Connected Port:", self.cursor.fetchone())

    def login_user(self, username, password):

        try:

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

            # DEBUG
            print("User Record:", user)

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
            failed_attempts = user[5]
            is_locked = user[6]

            # DEBUG
            print("Entered Password:", password)
            print("Stored Password:", stored_password)
            print("Password Length:", len(stored_password))
            print("Failed Attempts:", failed_attempts)
            print("Is Locked:", is_locked)

            # Account locked
            if is_locked:
                return {
                    "status": False,
                    "message": "Account Locked. Contact Administrator."
                }

            # Password verification
            match = bcrypt.checkpw(
                password.encode(),
                stored_password.encode()
            )

            # DEBUG
            print("Password Match:", match)

            if match:

                self.cursor.execute(
                    """
                    UPDATE users
                    SET failed_attempts = 0,
                        last_login = NOW()
                    WHERE user_id = %s
                    """,
                    (user_id,)
                )

                self.connection.commit()

                self.cursor.execute(
                    """
                    INSERT INTO login_logs(
                        user_id,
                        status
                    )
                    VALUES(%s,'SUCCESS')
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

            else:

                self.cursor.execute(
                    """
                    UPDATE users
                    SET failed_attempts = failed_attempts + 1
                    WHERE user_id = %s
                    """,
                    (user_id,)
                )

                self.connection.commit()

                self.cursor.execute(
                    """
                    SELECT failed_attempts
                    FROM users
                    WHERE user_id = %s
                    """,
                    (user_id,)
                )

                attempts = self.cursor.fetchone()[0]

                self.cursor.execute(
                    """
                    INSERT INTO login_logs(
                        user_id,
                        status
                    )
                    VALUES(%s,'FAILED')
                    """,
                    (user_id,)
                )

                self.connection.commit()

                if attempts >= 5:

                    self.cursor.execute(
                        """
                        UPDATE users
                        SET is_locked = 1
                        WHERE user_id = %s
                        """,
                        (user_id,)
                    )

                    self.connection.commit()

                    print("ACCOUNT LOCKED")

                    return {
                        "status": False,
                        "message": "Account Locked After 5 Failed Attempts"
                    }

                print("LOGIN FAILED")

                return {
                    "status": False,
                    "message": f"Incorrect Password ({attempts}/5)"
                }

        except Exception as err:

            print("ERROR:", err)

            return {
                "status": False,
                "message": str(err)
            }

    def close_connection(self):

        if self.cursor:
            self.cursor.close()

        if self.connection:
            self.connection.close()
