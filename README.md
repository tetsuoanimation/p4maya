# p4maya
A simple wrapper for perforce cmd and plugin to use perforce within maya

![grafik](https://user-images.githubusercontent.com/58070351/232020931-b5523b9c-7671-433a-b136-226eb33c05f9.png)


## Usage:
To use it in maya, put it into your scripts folder and run
``` 
p4plugin = p4maya.MayaP4Plugin()
p4plugin.buildMenu()
```

This will create a menu called 'perforce'. 
- Use 'Setup Connection' to set up your connection.
- Use the Submit / Add /Sync functions to interface with perforce

## Notes:
- When you use the menu to sync alembic files, they will be unloaded before sync and reloaded afterwards to ensure they are downloaded.
- Credentials are saved in the system PATH - this is the same way that perforce cmd stores it. However, this stores your password in cleartext and might be considered unsave by some pipelines.
