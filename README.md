# Hyundai-USA-Inventory-Locator

How to use
-------------

Download Release file to get Mac Application & Windows Executable. It is under /ElantraN/Executables.

History
-------------

2022-04-22 Started Project, Finished Elantra N version

## If you want to customize the program (setting the default selection)

0. Install python (at least 3.10) and pip

https://www.python.org/downloads/

https://phoenixnap.com/kb/install-pip-windows

1. Open Elantra.py

2. Line 67, enter your zipcode
   
   ```
   zipText.insert(0,"11111")
   ```

3. Line 78, enter exterior color
   
   ```
   zipText.insert(0,"Cyber Gray")
   ```
   
   Selections are (Case Sensitive):
* Performance Blue

* Cyber Gray

* Phantom Black

* Ceramic White

* Intense Blue
4. Line 78, enter exterior color
   
   ```
   if TransDict[i] == "Manual":
   ```
   
   Selections are (Case Sensitive):
* Automatic

* Manual
5. Save and exit

6. Locate your termial to the folder where Elantra.py is.

7. Install pyinstaller
   
   ```
   pip install pyinstaller
   ```

8. Make executable

```
pyinstaller -w -F ElantraN.py
```

9. You will have your working program under dist folder. You can erase the rest.
