from rich import print as pprint

import funcs as func
import messages as message
import oper
import token_op


def main():
    func.set_title("PortIO 命令行启动器 - Build 2023.02")
    func.clear_screen()
    print(message.WELCOME)
    token_str = token_op.read_token()
    while True:
        if token_str is None:
            pprint(message.OPERATION_NO_TOKEN)
        else:
            pprint(message.OPERATION_TOKEN)
        op = input("")
        try:
            op = int(op)
        except ValueError:
            func.error("输入不合法")
            func.pause_and_exit()
        if token_str is None:
            if op == 0:
                func.exit()
            elif op == 1:
                oper.update_token()
                oper.start_tunnel()
            else:
                func.error("输入不合法")
                func.pause_and_exit()
        else:
            if op == 0:
                func.exit()
            elif op == 1:
                oper.list_tunnels()
            # elif op == 2:
            #     pass
            elif op == 2:
                oper.signin()
            elif op == 3:
                oper.start_tunnel()
            elif op == 8:
                oper.download_frp()
            elif op == 9:
                oper.update_token()
            else:
                func.error("输入不合法")
                func.pause_and_exit()


if __name__ == '__main__':
    main()
