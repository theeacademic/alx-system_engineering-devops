# Puppet Manifest for configuring Apache and ensuring a specific configuration file exists

# Exec resource to create a missing Apache config file
exec { 'create_missing_config':
  command => '/bin/echo "Configuration content" > /etc/apache2/sites-available/missing-config.conf',
  creates => '/etc/apache2/sites-available/missing-config.conf',
}

# File resource to enable the created config file
file { 'enable_config':
  path    => '/etc/apache2/sites-enabled/missing-config.conf',
  ensure  => 'link',
  target  => '/etc/apache2/sites-available/missing-config.conf',
  require => Exec['create_missing_config'],
}

# Service resource to ensure Apache is running and enabled
service { 'apache2':
  ensure    => 'running',
  enable    => true,
  subscribe => File['enable_config'],
  provider  => 'systemd',  # Specify systemd as the service provider if using systemd-based systems
}

