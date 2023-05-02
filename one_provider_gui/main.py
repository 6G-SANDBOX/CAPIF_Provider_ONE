
from cmd import Cmd
from capif_ops.provider_previous_register import PreviousRegister
from capif_ops.provider_register_capif import RegisterProvider
from capif_ops.provider_aef_publish_service import  PublishService
from capif_ops.provider_delete import RemoveProvider
from capif_ops.provider_get_auth import PreviousAuth
from capif_ops.provider_aef_remove_service import RemoveService
import shlex
import subprocess
from art import *
from termcolor import colored

prev_register = PreviousRegister()
regiter_capif = RegisterProvider()
publish_service = PublishService()
remove_provider = RemoveProvider()
remove_service = RemoveService()
provider_auth = PreviousAuth()


class CAPIFProvider(Cmd):

  def __init__(self):
        Cmd.__init__(self)
        self.prompt = "> "
        self.intro = tprint("Welcome  to  Provider Console")

  def emptyline(self):
        """Do nothing on empty input line"""
        pass

  def preloop(self):
    state = prev_register.execute_previous_register_provider()
    self.previous_register_state = state

  def precmd(self, line):

    line = line.lower()
    args = shlex.split(line)

    if len(args) >= 1 and args[0] in ["goodbye"]:
        print("The first argument is username")
        return ""

    elif len(args) >= 1 and args[0] not in ["->", "wall", "follows", "exit", "help"]:
        pass

    return line

  def do_register_provider(self, input):
    'Register a provider to CAPIF instance'
    regiter_capif.execute_register_provider(input)

  def do_publish_service(self, input):
    'Publish Service in CAPIF'
    publish_service.execute_publish(input)

  def do_provider_get_auth(self, input):
    'Get jwt token to register provider in CAPIF (Optional, only if token expires)'
    provider_auth.execute_get_auth()

  def do_get_ca_root(self, input):
      pass

  def do_remove_service(self, input):
    'Remove published service in CAPIF'
    remove_service.execute_remove(input)

  def do_remove_provider(self, input):
    'Remove provider registered from CAPIF'
    remove_provider.execute_remove_provider(input)

  def do_exit(self, input):
    'Exit program'
    print('\nExiting...')
    return True


if __name__ == '__main__':
    try:
        CAPIFProvider().cmdloop()
    except KeyboardInterrupt:
        print('\nExiting...')