# 0-strace_is_your_friend.pp
exec { 'create_missing_config':
  command => '/bin/echo "Configuration content" > /etc/apache2/sites-available/missing-config.conf',
  creates => '/etc/apache2/sites-available/missing-config.conf',
}

file { 'enable_config':
  path    => '/etc/apache2/sites-enabled/missing-config.conf',
  ensure  => 'link',
  target  => '/etc/apache2/sites-available/missing-config.conf',
  require => Exec['create_missing_config'],
}

service { 'apache2':
  ensure    => 'running',
  enable    => true,
  subscribe => File['enable_config'],
}

