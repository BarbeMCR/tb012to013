#!/usr/bin/env python3

# Copyright (c) 2022 BarbeMCR
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

def main():
    import shelve
    import os
    import datetime
    import random
    import hashlib
    import time
    import sys

    """This utility converts legacy BarbeMCR's The Betrothed 0.12 savefiles to BarbeMCR's The Betrothed 0.13 ones that can be upgraded in-game."""
    
    print("This utility converts legacy BarbeMCR's The Betrothed 0.12 savefiles to 0.13 savefiles that can be upgraded in-game.")
    print("During the conversion, the current time will be used for the creation and access time.")
    print("Also, a dummy RNG status will be inserted. However, this shouldn't have any bad consequence during gameplay.")

    def ask_input():
        """Return a savefile path taken from user input."""
        savefile_path = input("Insert a valid path leading to a BarbeMCR's The Betrothed 0.12 savefile (without any extension): ")
        if os.path.isfile(savefile_path + '.dat'):
            return savefile_path
        else:
            print(f"Savefile {savefile_path} doesn't exist.")
            ask_input()

    savefile_path = ask_input()

    savefile = shelve.open(savefile_path)
    if savefile['version'] != 7130:
        # Check if the savefile version isn't 0.12
        print(f"File {savefile_path} isn't a BarbeMCR's The Betrothed 0.12 savefile.")
        print(f"Instead, it is a BarbeMCR's The Betrothed build {savefile['version']} savefile (or equivalent).")
        savefile.close()
        print("The utility will restart in 5 seconds. Make sure to input a valid BarbeMCR's The Betrothed 0.12 savefile!")
        time.sleep(5)
        os.execv(sys.executable, ['python'] + sys.argv)
    else:
        # Perform the upgrade by adding the missing tags and updating the variable format
        savefile['version'] = 8050
        savefile['creation_version'] = 7130
        savefile['creation_time'] = datetime.datetime.now().strftime('%B %d %Y, %H:%M:%S')
        savefile['access_time'] = savefile['creation_time']
        savefile['rng'] = random.getstate()
        savefile['health'] = {'renzo': savefile['health']}
        savefile['energy'] = {'renzo': savefile['energy']}
        savefile['energy_overflow'] = {'renzo': savefile['energy_overflow']}
        savefile.close()
        hash = hashlib.sha256()
        with open(savefile_path + '.dat', 'rb') as savefile:
            hash.update(savefile.read())
            with open(savefile_path + '.checksum', 'w') as checksum:
                checksum.write(hash.hexdigest())
        print("The upgrade was completed.")
        print(f"Now it is possible to load {savefile_path} in BarbeMCR's The Betrothed 0.13 (or higher).")
        sys.exit()

if __name__ == '__main__':
    main()