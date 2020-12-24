from telloUDP import SimpleTelloUDP
from time import sleep
from pickle import load, dump

# try:
#     wifiTellos = load(open('wifiTellos.p','rb'))
#
# except:
#     wifiTellos = {}
#     dump(wifiTellos,open('wifiTellos.p','wb'))

ssid = input('Please enter the SSID of the Wifi Network: ')
password = input('Please enter the Password of the Wifi Network: ')

flag = True
while flag:
    print()
    input('Please power on your Tello.\nPress ENTER to Continue...')
    print()
    input('Please connect your computer to your Tello.\nPress ENTER to Continue...')

    print()
    #name = input('Please enter a name for this Tello: ')
    name = 'tello'
    print('\n\nNow connecting to {}...'.format(name))

    tello = SimpleTelloUDP('192.168.10.1',startWithData=False)

    recv1 = tello.send('command')
    if recv1 != False:
        print(recv1[0].decode())
        print('Configuring {}...'.format(name))

        sleep(2)

        recv2 = tello.send('ap ' + ssid + ' ' + password)
        if recv2 != False:
            print(recv2[0].decode())
        else:
            print('\n\n\nError in configuration.\nEnsure {} is powered on, hold the power button for 5 seconds, and try again.'.format(name))
    else:
        print('\n\n\nError entering command mode.\nEnsure {} is powered on, hold the power button for 5 seconds, and try again.'.format(name))
        break

    # if recv1[0].decode() == 'ok' and recv2[0].decode() == 'OK,drone will reboot in 3s':
    #     print()
    #     input('{0} is now ready to connect to WiFi. Ensure {0} is powered on.\nPress ENTER to Continue...'.format(name))
    #     print('Check your Wifi Router for the IP of {}. If it does not appear, enter N.'.format(name))
    #     ip = input('Please enter the IP: ')
    #
    #     if ip.lower() == 'n':
    #         print('\nCheck your SSID and Password.\nEnsure {} is powered on, hold the power button for 5 seconds, and try again.'.format(name))
    #         break
    #     else:
    #         wifiTellos[name] = ip
    #         dump(wifiTellos, open('wifiTellos.p', 'wb'))
    #         print()
    input('{0} configuration complete! Please power down {0}.\nPress ENTER to Continue...'.format(name))




    print()
    info = input('Would you like to configure another Tello (Y/N): ')
    if info.lower() != 'y':
        flag = False

print('\n\nTello Wifi Connector Complete.\nGoodbye!')

