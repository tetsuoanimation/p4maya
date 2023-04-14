import os, sys
import pymel.core as pm
if sys.version_info[0]>2:
    from importlib import reload

import perforceHelpers
reload( perforceHelpers )
from perforceHelpers import P4Connection


class MayaP4Plugin():
    def __init__(self, userConfig=None):
        self.userConfig = userConfig
        self.conn = P4Connection()
        print(self.conn.info())
        if userConfig:
            self.updateConnection(self.userConfig.p4port, self.userConfig.p4user, self.userConfig.p4workspace, self.userConfig.p4pass)
        
    def reloadConnection(self, userConfig=None):
        self.userConfig = userConfig
        self.updateConnection(self.userConfig.p4port, self.userConfig.p4user, self.userConfig.p4workspace, self.userConfig.p4pass)
    
    def buildMenu(self):
        mainWindow = pm.language.melGlobals['gMainWindow']
        menuObj = 'PerforceToolsMenu'
        menuLabel = 'Perforce'

        if pm.menu(menuObj, label=menuLabel, exists=True, parent=mainWindow):
            pm.deleteUI(pm.menu(menuObj, edit=True, deleteAllItems=True))

        perforceMenu = pm.menu(menuObj, label=menuLabel, parent=mainWindow, tearOff=True)

        pm.menuItem(label='Open P4V', command= lambda *args: self.openP4V())

        pm.menuItem(label='Get Latest', subMenu=True, parent=perforceMenu, tearOff=True)
        pm.menuItem(label='Sync Current Scene', command= lambda *args: self.syncScene())
        pm.menuItem(label='Sync Current Folder', command= lambda *args: self.syncFolder())
        pm.menuItem(label='Sync References', command= lambda *args: self.syncReferences())
        pm.menuItem(label='Sync And Reload References', command= lambda *args: self.syncReloadReferences())
        pm.setParent('..', menu=True)

        pm.menuItem(label='Checkout', subMenu=True, parent=perforceMenu, tearOff=True)
        pm.menuItem(label='Checkout Current Scene', command= lambda *args: self.checkoutScene())
        pm.menuItem(label='Checkout Current Folder', command= lambda *args: self.checkoutFolder())
        pm.menuItem(label='Dump Checked Out Files', command= lambda *args: self.dumpCheckedOut())
        pm.setParent('..', menu=True)

        pm.menuItem(label='Add', subMenu=True, parent=perforceMenu, tearOff=True)
        pm.menuItem(label='Add Current Scene', command= lambda *args: self.addScene())
        pm.menuItem(label='Add Current Folder', command= lambda *args: self.addFolder())
        pm.menuItem(label='Add And Submit Scene', command= lambda *args: self.addSubmitScene())
        pm.setParent('..', menu=True)

        pm.menuItem(label='Submit', command= lambda *args: self.submit())
        pm.setParent('..', menu=True)

        pm.menuItem(label='Dump Info', command= lambda *args: self.dumpInfo())
        pm.setParent('..', menu=True)

        pm.menuItem(label='Setup Connection', command= lambda *args: self.setupConnection())
        pm.menuItem(label='Reload Settings', command= lambda *args: self.reloadConnection())
        pm.setParent('..', menu=True)


    def openP4V(self):
        self.conn.visual()

    def syncScene(self):
        scenePath = pm.sceneName()
        if scenePath:
            print('Syncing {} from P4...'.format(scenePath))
            print(self.conn.sync(scenePath))
            print('Syncing done')
        else:
            print('No Scene open')

    def syncFolder(self):
        scenePath = pm.sceneName()
        if scenePath:
            scenePath = os.path.dirname(scenePath)
            print('Syncing {} from P4...'.format(scenePath))
            print(self.conn.sync(scenePath))
            print('Syncing done')
        else:
            print('No Scene open')

    def syncReferences(self):
        
        refList = pm.listReferences(loaded=True, unloaded=False, refNodes=True)
        refNodes = [pm.FileReference(refnode=ref[0]) for ref in refList]
        
        refPaths = []
        unloadedRefs = []
        for ref in refNodes:
            path = ref.path
            if path.endswith(".abc"):
                ref.unload()
                unloadedRefs.append(ref)
            if path not in refPaths:
                refPaths.append(path)

        for path in refPaths:      
            print("Syncing {} from P4...".format(path))     
            print(self.conn.sync(path))

        for unloadedRef in unloadedRefs:
            unloadedRef.load()
            
        print("All references synced from P4")
    
    def syncReloadReferences(self):
        refList = pm.listReferences(loaded=True, unloaded=False, refNodes=True)
        refNodes = [pm.FileReference(refnode=ref[0]) for ref in refList]
        
        refPaths = []
        for ref in refNodes:
            path = ref.path
            ref.unload()
            if path not in refPaths:
                refPaths.append(path)

        for path in refPaths:
            print("Syncing {} from P4...".format(path))     
            print(self.conn.sync(path))
        print("All references synced from P4")

        for ref in refNodes:
            ref.load()

    def checkoutScene(self):
        scenePath = pm.sceneName()
        if scenePath:
            print('Checking Out {} from P4...'.format(scenePath))
            print(self.conn.checkout(scenePath))
            print('Checked out')
        else:
            print('No Scene open')

    def checkoutFolder(self):
        scenePath = pm.sceneName()
        if scenePath:
            scenePath = os.path.dirname(scenePath)
            print('Checking Out {} from P4...'.format(scenePath))
            print(self.conn.checkout(scenePath))
            print('Checked out')
        else:
            print('No Scene open')

    def dumpCheckedOut(self):
        print(self.conn.getOpen())

    def addScene(self):
        scenePath = pm.sceneName()
        if scenePath:
            print('Adding {} to P4...'.format(scenePath))
            print(self.conn.add(scenePath))
            print('Added')
        else:
            print('No Scene open')
        
    def addFolder(self):
        scenePath = pm.sceneName()
        scenePath = os.path.dirname(scenePath)
        if scenePath:
            print('Adding {} to P4...'.format(scenePath))
            print(self.conn.add(scenePath))
            print('Added')
        else:
            print('No Scene open')
        
    def addSubmitScene(self):
        scenePath = pm.sceneName()
        pm.saveFile()
        self.addScene()
        self.submit()

    def submit(self):
        print('scene name is {}'.format(pm.sceneName()))
        print('submitting v1')
        if pm.sceneName():
            
            if self.conn.getOpen():
                changeDlg = pm.promptDialog(title="Changelist", message="Please state the changes you are \nsubmitting", scrollableField=True, button=["Submit","Cancel"], defaultButton="Submit", cancelButton="Cancel", dismissString="Cancel")
                if changeDlg == "Submit":
                    change = pm.promptDialog(query=True, text=True)
                    while change == "" and changeDlg== "Submit":
                        changeDlg = pm.promptDialog(title="Changelist", message="Cannot submit empty changelist! \nPlease state the changes you are submitting \nor press cancel", scrollableField=True, button=["Submit","Cancel"], defaultButton="Submit", cancelButton="Cancel", dismissString="Cancel")
                        change = pm.promptDialog(query=True, text=True)
                    if changeDlg == "Submit":
                        if os.path.basename(pm.sceneName()) in self.conn.getOpen():
                            print ("Adding change {}".format( change ))
                            print('Submitting scene ...')
                            pm.saveFile()
                            self.conn.submit(d=change, path=pm.sceneName())
                        else:
                            print('Current scene is not checked out, ignoring for submit')
                    else:
                        print ("Change has been canceled by User")
                else:
                    print('Operation Canceled')
        else:
            print('Cannot submit startup scene')

    def dumpInfo(self):
        print(self.conn.info())
    
    def setupConnection(self):
        window = "p4_setup_connection_window"
        if pm.window(window, exists=True):
            pm.deleteUI(window)
        pm.window(window, title="P4 Connection Setup")
        pm.columnLayout(adjustableColumn=True)
        
        serverTextGrp= pm.textFieldGrp(label="P4 Server", placeholderText='PERFORCE:1666')
        nameTextGrp= pm.textFieldGrp(label="P4 Username")
        clientTextGrp = pm.textFieldGrp(label="P4 Workspace")
        passwordTextGrp = pm.textFieldGrp(label="P4 Password")
        saveButton = pm.button(label="Save Connection", command=lambda *args: (self.updateConnection(serverTextGrp.getText(), nameTextGrp.getText(), clientTextGrp.getText(), passwordTextGrp.getText())))

        pm.showWindow(window)

    def updateConnection(self, server, user, client, password):
        print( user, client, password )
        if not server:
            server='PERFORCE:1666'
        self.conn.serverAddress = server
        self.conn.user = user
        self.conn.workspace = client
        self.conn.password = password

        self.conn.connect()
        self.dumpInfo()

if __name__ == "__main__":
    # Usage within maya
    p4plugin = p4maya.MayaP4Plugin()
    p4plugin.buildMenu()

    # you can also build a userConfig object and supply it to the connection
    # it is a simple object that has parameters for the login info. We are using a
    # namedtuple here but you can supply your own objects
    from collections import namedtuple
    UserConfig = namedtuple("UserConfig" "p4port, p4user, p4workspace, p4pass") #create the class
    userConfig = UserConfig("perforce:1666", "username", "workspace", "password") # instanciate with values
    conn_with_settings = P4Connection(userConfig)

    p4plugin_with_settings = MayaP4Plugin(userConfig=conn_with_settings)
    p4plugin_with_settings = p4maya.MayaP4Plugin()
    p4plugin_with_settings.buildMenu()