class OsTwoFa:

    def __init__(self):
        self.active = False

    def start2FA(self):
        import OSFA
        import threading
        try:
            threading.Thread(target=OSFA.startServer).start()
            self.active = True
        except:
            pass

    def reset2fa(self):
        import os
        try:
            os.remove("active.key")
            os.remove("token.tk")
        except FileNotFoundError:
            pass

    def checkKey(self, key):
        import os

        if not self.active:
            raise Exception("You cannot check the 2FA key without starting the 2FA server")
            return

        if not os.path.exists("active.key"):
            raise FileNotFoundError("The shared resource could not be found: active.key")
            return

        with open("active.key") as f:
            if str(key) == f.read():
                return True
            else:
                return False
