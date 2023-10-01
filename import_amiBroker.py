import os
import sys
import glob
import win32com.client

# Define import table as a list of dictionaries
imp_tbl = [
    {
        'db': r"C:\Program Files\AmiBroker\Zerodah",
        'data': r"D:\Quote-Equity-RELIANCE-EQ-30-08-2023-to-30-09-2023.csv",
        'format': r"wizard.format"
    },
]

def ImportData(ab, lst):
    for l in lst:
        print("Loading database {}".format(os.path.split(l['db'])[1]))
        ab.LoadDatabase(l['db'])
        f_lst = sorted(set(glob.glob(l['data'])))
        for f in f_lst:
            try:
                print("Importing datafile {}, using format {}".format(f, l['format']))
                ab.Import(0, f, l['format'])
            except Exception as e:
                print(f"Error importing datafile {f}: {str(e)}")
            else:
                (newpath, filename) = os.path.split(f)
                archive_folder = os.path.join(newpath, "archive")
                os.makedirs(archive_folder, exist_ok=True)
                os.rename(f, os.path.join(archive_folder, filename))
                print("Import complete")

        print("Saving Amibroker")
        ab.RefreshAll()
        ab.SaveDatabase()
        print("OK")

def main():
    oAB = win32com.client.Dispatch("Broker.Application")
    ImportData(oAB, imp_tbl)
    print("Terminated")
    oAB.Quit()
    return 0

if __name__ == '__main__':
    sys.exit(main())
