import json
import os
import shutil
import zipfile

import requests
from rich import print as pprint
from tqdm import tqdm

import config
import funcs as func
import token_op


def download_frp():
    if os.path.exists("frpc.exe"):
        func.error("已经有 Frp 客户端了")
    else:
        func.success("正在下载 Frp Zip 文件")
        response = requests.get("https://r2.laecloud.com/MEFrpRelease/MirrorEdgeFrp_0.46"
                                ".1_beta_windows_amd64.zip",
                                stream=True)
        process_bar = tqdm(colour='blue',
                           total=round(int(response.headers['content-length']) / 1024 ** 2, 2),
                           unit='MB',
                           desc="MirrorEdgeFrp.zip",
                           initial=0)  # 进度条的设置
        with open('MirrorEdgeFrp.zip', 'wb') as f:
            for part in response.iter_content(1024 ** 2):
                process_bar.update(1)
                f.write(part)
        func.success("完成")
        func.success("正在解压 Zip 文件")
        with zipfile.ZipFile("MirrorEdgeFrp.zip", "r") as zip_ref:
            zip_ref.extractall("./")
        func.success("完成")
        func.success("正在重命名 Zip 文件")
        os.rename("frp_MirrorEdgeFrp_0.46.1_beta_windows_amd64", "frp")
        func.success("完成")
        func.success("正在删除 Zip 文件")
        os.remove("MirrorEdgeFrp.zip")
        func.success("完成")
        func.success("正在移动 Frp 客户端")
        os.rename("frp/frpc.exe", "frpc.exe")
        func.success("完成")
        func.success("正在删除目录")
        shutil.rmtree("frp")
        func.success("完成")


def update_token():
    tk = func.pinput("请输入 Token: ")
    token_op.write_token(tk)


def list_tunnels(mode="ok"):
    response = requests.get(f"{config.BASE_URL}/tunnels", headers=config.get_headers())
    response.encoding = response.apparent_encoding
    resp_json = json.loads(response.text)
    if len(resp_json) == 0:
        func.warning("此账户下暂无隧道")
        if mode == "not ok":
            func.pause_and_exit()
    else:
        for i in range(0, len(resp_json)):
            pprint(
                f"[reset][bold blue]{resp_json[i]['id']}[/bold blue][bold white])[/bold white][/reset] [bold green]{resp_json[i]['name']}[/bold green]")
        func.wait()


def signin():
    response = requests.post(f"{config.BASE_URL}/traffic", headers=config.get_headers())
    response.encoding = response.apparent_encoding
    resp_json = json.loads(response.text)
    try:
        if resp_json["message"]:
            func.error(resp_json["message"])
    except KeyError:
        func.success(f"签到成功, 获得 {resp_json['traffic']} GB 流量!")
    func.wait()


def start_tunnel():
    if not os.path.exists("frpc.exe"):
        download_frp()
    func.clear_screen()
    list_tunnels(mode="not ok")
    tunnel_id = int(func.pinput("请输入隧道 ID: "))
    response = requests.get(f"{config.BASE_URL}/tunnels", headers=config.get_headers())
    response.encoding = response.apparent_encoding
    resp_json = json.loads(response.text)
    flag = False
    for i in range(0, len(resp_json)):
        if resp_json[i]['id'] == tunnel_id:
            flag = True
    if not flag:
        func.error("隧道 ID 输入错误")
        func.pause_and_exit()
    if not os.path.exists("config"):
        os.mkdir("config")
    response = requests.get(f"{config.BASE_URL}/tunnels/{str(tunnel_id)}", headers=config.get_headers())
    response.encoding = response.apparent_encoding
    resp_json = json.loads(response.text)
    config_content = f"{resp_json['config']['server']}\n\n{resp_json['config']['client']}"
    with open(f"config/{resp_json['name']}_config.ini", 'w') as f:
        f.write(config_content)
    os.system(f"start cmd.exe /k frpc.exe -c config/{resp_json['name']}_config.ini")
    func.success("启动成功, 您可以关闭本启动器!")
