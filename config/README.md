# Setting up the bare repo on the server side

In order to be able to deploy on push, we need to install a bare repo on the
server.

```
git init --bare predikon.git
cd predikon.git/hooks/
touch post-receive
chmod +x post-receive
```

The `post-receive` script contains the following:

```
#!/bin/bash

# Remove old content.
rm -rf /var/www/predikon/*
rm -rf /var/www/predikon-dev/*

# Export git content.
cd /var/www/predikon.git
git archive --format=tar master:predikon/ | tar -C /var/www/predikon -xf -
git archive --format=tar develop:predikon/ | tar -C /var/www/predikon-dev -xf -

# Reload apache.
# sudo apache2ctl graceful
sudo systemctl restart apache2
```

Finally, make sure the folders we just created belong to the `predikon` user:

```
chown -R predikon: [folder]
```

# Set sudo for predikon user

From root user, edit the sudoers:

```
visudo
```

And add the following line after `%root ALL=(ALL:ALL) ALL`:

```
predikon ALL=(ALL) NOPASSWD: /bin/systemctl restart apache2
```

# Setup on development machines

Then, once this is setup on the server, developers need to add it as a remove on
their machine:

```
git remote add production \
ssh://predikon@indy-predikon.epfl.ch/var/www/predikon.git
```

They can then simply push changes to the server, and the website will be
updated:

```
git push production master
```

# Apache config on the server

To enable caching of json content, add this line to
`/etc/apache2/mods-available/deflate.conf`:

```
AddOutputFilterByType DEFLATE application/json
```

## Enable mods

Run:

```
a2enmod
```

In the prompt enter:

```
wsgi status env mime alias auth_basic authn_file authz_default authz_groupfile
authz_host authz_user autoindex cgid deflate dir negotiation reqtimeout setenvif
```

And finally:

```
systemctl reload apache2
```

## Add sites

In `/etc/apache2/sites-available` add the following two symbolic links:

```
ln -s /opt/www/predikon-dev/config/apache-dev.config predikon-dev.conf
ln -s /opt/www/predikon/config/apache-config predikon.conf
```

## Enable sites

Run:

```
a2ensite predikon-dev
a2ensite predikon
systemctl reload apache2
```


