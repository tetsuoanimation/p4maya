import subprocess, os, re

class P4Connection():
    def __init__(self, user=None, serverAddress=None, workspace=None):
        self.user = user
        self.workspace = workspace
        self.serverAddress = serverAddress
        self.password = ''

        self.p4_runner = CommandRunner('P4')
        self.p4vc_runner = CommandRunner('P4VC')

    def connect(self):
        '''this just sets the variables to get ready to connect'''
        if self.user and self.serverAddress and self.workspace:
            print(self.p4_runner.run('set P4PORT={}'.format(self.serverAddress)))
            print(self.p4_runner.run('set P4USER={}'.format(self.user)))
            print(self.p4_runner.run('set P4CLIENT={}'.format(self.workspace)))
            print(self.p4_runner.run('set P4PASSWD={}'.format(self.password)))

    def sync(self, filename):
        if not os.path.isfile(filepath):
            filepath = '{}{}{}'.format(filepath, os.path.sep, '...')
        if filename:
            return self.p4vc_runner.run('sync {}'.format(filename))
        else:
            return False
    
    def info(self):
        return self.p4_runner.run('info')

    def filelog(self, filepath):
        if not os.path.isfile(filepath):
            filepath = '{}{}{}'.format(filepath, os.path.sep, '...')
        return self.p4vc_runner.run('filelog {}'.format(filepath))
    
    # def sync(self, filepath):
    #     if not os.path.isfile(filepath):
    #         filepath = '{}{}{}'.format(filepath, os.path.sep, '...')
    #     return self.p4_runner.run('sync {}'.format(filepath))

    def submit(self, d="p4 maya default change", path=None):
        if path is not None:
            print ('submitting path {}'.format(path))
            return self.p4_runner.run('submit -d \"{}\" {}'.format(d, path))
        else:
            return self.p4_runner.run('submit -d \"{}\"'.format(d))

    def add(self, filepath):
        if os.path.isfile(filepath):
            checkFile = self.p4_runner.run('files {}'.format(filepath))
            if not checkFile:
                return self.p4_runner.run('add {}'.format(filepath))
        else:
            output = []
            folderContents = [os.path.join(filepath, x) for x in os.listdir(filepath)]
            for item in folderContents:
                output.append(self.add(item))

            outMessage = ''
            for item in output:
                if item is not None:
                    outMessage += str(item)
            print (outMessage)

    def checkout(self, filepath):
        if not os.path.isfile(filepath):
            filepath = '{}{}{}'.format(filepath, os.path.sep, '...')
        return self.p4_runner.run('edit {}'.format(filepath))

    def revert(self, filepath):
        if not os.path.isfile(filepath):
            filepath = '{}{}{}'.format(filepath, os.path.sep, '...')
        return self.p4_runner.run('revert {}'.format(filepath))

    def getOpen(self):
        return self.p4_runner.run('opened')

    def visual(self):
        cmdCall = 'p4v'
        os.system(cmdCall)

class CommandRunner():
    def __init__(self, executable='cmd'):
        self.executable = executable

    def run(self, command, blocking=True):
        cmdCall = '{} {}'.format(self.executable, command)
        p = subprocess.Popen(cmdCall, stdout=subprocess.PIPE, shell=True)
        
        if blocking:
            out, err = p.communicate()
            return out.decode()
        else:
            pass
            # ok , this still blocks, but it blocks differently lol
            # data = p.stdout.readline()
            # out = []
            # while data:
            #     out.append (data.strip())
            #     data = p.stdout.readline()



if __name__  == '__main__':
    runner = CommandRunner('ls')
    print(runner.run('.', blocking=True))

    # this is just for testing - please don't run it without understanding
    path = os.path.dirname(__file__)

    # this is using the connection from PATH
    conn = P4Connection()
    print(conn.info())
    # print(conn.visual())
    # print(conn.sync(path))
    # print(conn.checkout(path))
    # print(conn.add(path))
    # print(conn.getOpen())
    # print(conn.submit())
    # print(conn.revert(path))


        