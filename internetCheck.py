#!/usr/bin/env python3
import gi
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Gtk', '3.0')
import sys
import requests
import http.client
from gi.repository import Gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import GLib



class MyIndicator:
  def __init__(self):
    self.proxy={"http":"http://username:password@proxyServer:port"}
    self.proxy_uri="http://username:password@proxyServer:port"
    self.ind = appindicator.Indicator.new(
                "Test",
                "indicator-messages",
                appindicator.IndicatorCategory.APPLICATION_STATUS)
    self.ind.set_status (appindicator.IndicatorStatus.ACTIVE)
    self.ind.set_attention_icon("new-messages-red")
    self.menu = Gtk.Menu()

    item = Gtk.MenuItem()
    item.set_label("px45")
    item.connect("activate", self.px45)
    self.menu.append(item)

    item = Gtk.MenuItem()
    item.set_label("px16")
    item.connect("activate", self.px16)
    self.menu.append(item)

    item = Gtk.MenuItem()
    item.set_label("Exit")
    item.connect("activate", self.quit)
    self.menu.append(item)

    self.menu.show_all()
    self.ind.set_menu(self.menu)

  def getStatus(self):

    conn = http.client.HTTPSConnection("proxyServer", "port")
    headers = {}
    username="username"
    password="password"
    if username and password:
      auth = '%s:%s' % (username, password)
      headers['Proxy-Authorization'] = 'Basic ' + "< base64 encoded username:password >"
    host = 'www.google.co.in'
    port = 443
    conn.set_tunnel(host, port, headers)
    conn.request("GET", "/")
    response = conn.getresponse()
    # print(response.status, response.reason)
    return response.status

  def main(self):
    self.check_site()
    GLib.timeout_add_seconds(2, self.check_site)
    Gtk.main()

  def px45(self, widget):
    self.proxy={"http":"http://username:password@proxyServer:port"}
    self.proxy_uri="http://username:password@proxyServer:80"
  def px16(self, widget):
    #set your proxy here like above

  def check_site(self):
    status=self.getStatus()
    if status==200 or status==302:
      # print ("active")
      self.ind.set_label("Online","Online")
      self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)
      
    else:
      # print ("Inactive")
      self.ind.set_label("Offline","Offline")
      self.ind.set_status(appindicator.IndicatorStatus.ATTENTION)
      
    return True

  def quit(self, widget):
    Gtk.main_quit()

if __name__ == '__main__':
  indicator = MyIndicator();
  indicator.main();
