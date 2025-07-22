#!/usr/bin/env python3
import sys
import argparse
from azure_cli import check_login
from commands.initialization import inizio, coda
from commands.synchronization import preludio
from commands.scaling import crescendo, diminuendo
from commands.configuration import pianissimo
from commands.deployment import esecuzione

def main():
    result = check_login()
    if result:
        print("𝄠 You are logged in as", result["user"]["name"]);
    else:
        print("𝄠 You are not logged in, please run 'az login'");
        return

    if len(sys.argv) == 1 or sys.argv[1].startswith('-'):
        print("""
          @@@@      
         @    #     
         @   @@     
         , @@@      
        .@@@@       
      @@@@@         888b     d888                            888                  
    @@@&  @         8888b   d8888                            888                  
   @@.   #@@@@/     88888b.d88888                            888                  
  @@   @@  @  @@@   888Y88888P888  8888b.   .d88b.  .d8888b  888888 888d888 .d88b.
   @.  @.   \\  @@   888 Y888P 888     "88b d8P  Y8b 88K      888    888P"  d88""88b
     @___+=#@@      888  Y8P  888 .d888888 88888888 "Y8888b. 888    888    888  888
             %      888   "   888 888  888 Y8b.          X88 Y88b.  888    Y88..88P
      @@@@   /      888       888 "Y888888  "Y8888   88888P'  "Y888 888     "Y88P" 
     .@@@@*#@   
""")

    command_map = {
        'inizio': inizio,
        'preludio': preludio,
        'coda': coda,
        'pianissimo': pianissimo,
        'esecuzione': esecuzione,
        'crescendo': crescendo,
        'diminuendo': diminuendo,
    }
    
    parser = argparse.ArgumentParser(description="𝄠 Maestro is a tool to manage a swarm of Azure container apps", prog="maestro")
    subparsers = parser.add_subparsers(dest="command", title='Commands', description="𝄠 Select one. Run 'maestro {command} -h' to see details.", required=True)
    subparsers.add_parser("partitura", description="𝄚 Visualize local state", help="𝄚 Visualize local state")
    subparsers.add_parser("inizio", description="𝄊 Initialize local state", help="𝄊 Initialize local state")
    parser_repertorio = subparsers.add_parser("repertorio", description="𝄰𝄬 Manage apps", help="𝄰𝄬Manage apps")
    repertorio_subparsers = parser_repertorio.add_subparsers(dest="subcommand", help="𝄰𝄬 Select one. Run 'maestro repertorio {subcommand} -h' to see details.")
    parser_aggiungere = repertorio_subparsers.add_parser("aggiungere", description='𝄰 Add an ACA YAML to the local state.', help='𝄰 Add an ACA YAML to the local state.')
    parser_aggiungere.add_argument("file_path", help="The path to ACA YAML")
    parser_togliere = repertorio_subparsers.add_parser("togliere", description="𝄬 Remove an app from local state", help="𝄬 Remove an app from local state")
    parser_togliere.add_argument("app_name", help='The app name')
    subparsers.add_parser("preludio", description="𝄋 Synchronize local state with Azure", help="𝄋 Synchronize local state with Azure")
    subparsers.add_parser("coda", description="𝄌 Erase local state", help="𝄌 Erase local state")
    subparsers.add_parser("esecuzione", description="𝄆 Send local state to Azure", help="𝄆 Send local state to Azure")
    parser_crescendo = subparsers.add_parser("crescendo", description="𝆒 Increase scaling of an app", help="𝆒 Increase scaling of an app")
    parser_crescendo.add_argument('app_name', help='The app name')
    parser_crescendo.add_argument('incr', help='Value to increase by', type=int)
    parser_diminuendo = subparsers.add_parser("diminuendo", description="𝆓 Decrease scaling of an app", help="𝆓 Decrease scaling of an app")
    parser_diminuendo.add_argument('app_name', help='The app name')
    parser_diminuendo.add_argument('decr', help='Value to decrease by', type=int)
    parser_pianissimo = subparsers.add_parser("pianissimo", description="𝆏𝆏 Set a secret", help="𝆏𝆏Set a secret")
    parser_pianissimo.add_argument('app_name', help='The app name')
    parser_pianissimo.add_argument('secret_name', help='The name of the secret')
    parser_pianissimo.add_argument('value', help='The value to give to the secret')
    parser_valore = subparsers.add_parser("valore", description="𝅘𝅥𝅮 Set an environment value", help="𝅘𝅥𝅮 Set an environment value")
    parser_valore.add_argument('app_name', help='The app name')
    parser_valore.add_argument('var_name', help='The name of the variable')
    parser_valore.add_argument('value', help='The value to give to the variable')

    args = parser.parse_args()
    command_func = command_map.get(args.command)
    if command_func:
        command_func(args)
    else:
        print(f'𝄠 Not implemented yet: {args.command}')

if __name__ == "__main__":
    main()