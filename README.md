# network_asset_inventory_and_discovery

MY FOCUS:
- using more comments
- reducing duplicate / excess code blocks

My program should answer the following questions when used:

What devices exist on my network?
When did a new device appear?
Did an IP or hostname change?
Is something missing or suspicious?

It will do this by pinging devices on the network every 5-10 mins, using nmap and other packages which I will add to a list if I do use them.
If any suspicous activityis to occur, it will alert me using gmail/somrthing (not sure yet)

-------------------------------
main.py:
network_scan()  COMPLETE
normalize_results()
compare_with_db() 50% DONE (compare is complete, need to implement sus counter)
store_snapshot()
notify_changes()
-------------------------------
TO ADD:
store_snapshot()
notify_changes()
normalize_results()
user output to questions demonstrated above delieverd by gmail using api
