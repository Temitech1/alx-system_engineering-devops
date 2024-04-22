# setup client SSH configuration without password

exec { 'echo "PasswordAuthentication no\nIdentityFile ~/.ssh/school" >> /etc/ssh/ssh_config':
	path    => '/bin/'
}
