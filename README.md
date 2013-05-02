Bus-Stops-at-SGUL
=================

Simple page to display timely information about buses around the university

1. To run the backend harvesting, we suggest running the "cron.py" file with screen, nohup, supervise, or any other means you have to daemonize it. Note that this is a 24/7 constantly running script.
2. Put the ajaxreturn.php on any accessible location on your server
3. Put the web bit somewhere accessible as well (on the same server, or you'll need to fiddle with the header() )