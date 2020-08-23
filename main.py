import subprocess
import io
import time
import os


def download(mode, libs):
    print("开始下载")
    libs = libs.split()
    installed = 0
    url = "pip install "
    if mode == "temporary":
        url = "pip install -i https://pypi.tuna.tsinghua.edu.cn/simple "
    if "upgrade" in mode:
        url += "--upgrade "
    for i in libs:
        res = subprocess.Popen(url + i, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1)
        res.wait()
        stderr = io.TextIOWrapper(res.stderr, encoding='utf-8')
        s_stderr = str(stderr.read())
        if "No matching distribution found for " in s_stderr:
            print("[ERROR] 无法找到库:" + i)
        else:
            print("{}已安装成功".format(i))
            installed += 1
    print("预计下载{}个库  有{}个库安装成功  {}个库安装失败".format(len(libs), installed, len(libs) - installed))
    time.sleep(1)
    return "下载完成"


def query(mode):
    print("查询中...")
    if mode == "simple":
        res = subprocess.Popen("pip list", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=10000)
        res.wait()
        stderr = io.TextIOWrapper(res.stderr, encoding='utf-8')
        stdout = io.TextIOWrapper(res.stdout, encoding='utf-8')
        s_stdout = str(stdout.read())
        s_stderr = str(stderr.read())
        print(s_stdout)
        if "You are using pip version " in s_stderr:
            print("[Note] 您的pip版本可更新")
            sel = input("是否需要更新您的pip?[Y/N]: ").lower()
            if sel == 'y':
                update()
    if mode == "upgrade":
        res = subprocess.Popen("pip list --outdated", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               bufsize=-1)
        res.wait()
        stderr = io.TextIOWrapper(res.stderr, encoding='utf-8')
        stdout = io.TextIOWrapper(res.stdout, encoding='utf-8')
        s_stderr = str(stderr.read())
        s_stdout = str(stdout.read()).split('\n')[2:-1]
        if "You are using pip version " in s_stderr:
            print("[Note] 您的pip版本可更新")
            sel = input("是否需要更新您的pip?[Y/N]: ").lower()
            if sel == 'y':
                update()
        if not s_stdout:
            print("您没有可更新的库")
            return None
        print("以下是可更新的库")
        for i in range(len(s_stdout)):
            s_stdout[i] = s_stdout[i].split()
        for i in s_stdout:
            print(i[0])
        sel = input("是否需要更新?[Y/N]: ").lower()
        if not sel == 'y':
            return "已退出更新"
        print("开始更新...")
        download("upgrade", ' '.join([i[0] for i in s_stdout]))
        print("更新完毕")
    time.sleep(1)
    return "查询完毕"


def update():
    print("pip更新中...")
    res = subprocess.Popen("python -m pip install --upgrade pip", shell=True, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, bufsize=-1)
    res.wait()
    time.sleep(1)
    return "更新完成"


def uninstall(libs):
    print("开始卸载...")
    libs = libs.split()
    for i in libs:
        res = subprocess.Popen("pip uninstall " + i, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               bufsize=-1)
        res.wait()
        stderr = io.TextIOWrapper(res.stderr, encoding='utf-8')
        s_stderr = str(stderr.read())
        if "WARNING: Skipping" in s_stderr:
            print("[Error] 无法找到{}库".format(i))
    return "卸载完毕"


def tsinghua_install(mode):
    if mode == "uninstall":
        if os.path.exists("C:/Users/29358/pip/pip.ini"):
            print("正在删除...")
            os.remove("C:/Users/29358/pip/pip.ini")
            return "删除完毕"
        return "您尚未安装清华镜像配置文件，无需卸载"
    if mode == "install":
        text = "[global]\nindex-url = https://pypi.tuna.tsinghua.edu.cn/simple\n[install]\ntrusted-host = " \
               "https://pypi.tuna.tsinghua.edu.cn "
        if os.path.exists("C:/Users/29358/pip/pip.ini"):
            print("已检测到配置文件，正在分析文件完整性...")
            if open("C:/Users/29358/pip/pip.ini", 'r').read() == text:
                return "您已安装清华镜像配置文件，无需安装"
            print("您的配置文件不完整，正在重新配置...")
            open("C:/Users/29358/pip/pip.ini", 'w').write(text)
            return "配置完毕"
        print("检测到您尚未安装配置文件，正在安装...")
        open("C:/Users/29358/pip/pip.ini", 'w').write(text)
        return "配置完毕"


while True:
    print("PIP 管理器")
    print("1. 安装库")
    print("2. 查询库")
    print("3. 卸载库")
    print("4. 更新pip")
    print("5. 镜像设置")
    print("6. 关于")
    print("7. 退出")
    try:
        sel = int(input(">>>"))
    except ValueError:
        print("[Error] 输入的数值不合法")
    if sel == 1:
        print("\n安装")
        print("1. 普通方式安装 'pip install xxx'")
        print("2. 镜像安装")
        print("[Note] 若安装了配置文件，选哪个都一样")
        try:
            sel = int(input(">>>"))
            libs = input("请输入要安装的库。若有多个库需要安装，请用空格隔开:\n")
        except ValueError:
            print("[Error] 输入的数值不合法")
        if sel == 1:
            download("a", libs)
        elif sel == 2:
            download("temporary", libs)
    elif sel == 2:
        print("\n查询")
        print("1. 查询目前安装的库")
        print("2. 查询需要更新的库")
        try:
            sel = int(input(">>>"))
        except ValueError:
            print("[Error] 输入的数值不合法")
        if sel == 1:
            query("simple")
        elif sel == 2:
            query("upgrade")
    elif sel == 3:
        libs = input("请输入要卸载的库。若有多个库需要卸载，请用空格隔开:\n")
        uninstall(libs)
    elif sel == 4:
        update()
    elif sel == 5:
        print("\n镜像设置")
        print("1. 安装配置文件")
        print("2. 卸载配置文件")
        try:
            sel = int(input(">>>"))
        except ValueError:
            print("[Error] 输入的数值不合法")
        if sel == 1:
            tsinghua_install("install")
        elif sel == 2:
            tsinghua_install("uninstall")
        time.sleep(1)
    elif sel == 6:
        print("\n关于")
        print("作者: AuroraZiling")
        print("QQ: 2935876049")
        print("若有Bug或建议可以在Github或QQ找我")
        time.sleep(3)
    elif sel == 7:
        exit()
