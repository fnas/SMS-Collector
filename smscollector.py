#!/usr/bin/env python

from gi.repository import Gtk

UI_FILE = "main.ui"

class Smscollector:

  filenames = {
    "Worldwide": "lists/sms_all.txt",
    "North America": "lists/sms_usa.txt",
    "Europe": "lists/sms_eur.txt",
    "Japan": "lists/sms_jpn.txt",
    "Brazil": "lists/sms_bra.txt",
    "Other": "lists/sms_other.txt",
  }
  gameCount = 0
  statusid = 0
  database = ""
  savefile=""

  def __init__(self):
    self.builder = Gtk.Builder()
    self.builder.add_from_file(UI_FILE)
    self.builder.connect_signals(self)

    window = self.builder.get_object("window")
    window.show_all()
    self.aboutdialog = self.builder.get_object("aboutdialog")

    self.treeviewGames = self.builder.get_object("treeviewGames")
    self.liststoreGames = self.builder.get_object("liststoreGames")

    self.statusbar = self.builder.get_object("statusbar")

    #self.loadNewProject("lol")

    context_id = self.statusbar.get_context_id("test")
    self.statusid = self.statusbar.push(context_id, "")

  def destroy(self, window):
    Gtk.main_quit()

  def clicked_about(self, menuitem):
    response = self.aboutdialog.run()
    if response == Gtk.ResponseType.DELETE_EVENT or response == Gtk.ResponseType.CANCEL:
      self.aboutdialog.hide()

  def clicked_NewProject(self, menuitem):
    self.newProject(menuitem.get_children()[0].get_label())

  def newProject(self, region):
    self.liststoreGames.clear()
    self.gameCount = 0
    self.database = region

    file = open(self.filenames[self.database], "r")
    for line in file:
      item = self.liststoreGames.append([line.strip(), False, False, False])
      self.gameCount += 1
    file.close()

    self.updateStatus()

  def clicked_save(self, menuitem):
    if self.savefile != "":
      self.saveCollection(self.savefile)
    else:
      self.clicked_saveAs(menuitem)

  def clicked_saveAs(self, menuitem):
    dialog = Gtk.FileChooserDialog("Save collection as", menuitem.get_toplevel(), Gtk.FileChooserAction.SAVE)
    dialog.add_button(Gtk.STOCK_CANCEL, 0)
    dialog.add_button(Gtk.STOCK_SAVE, 1)
    dialog.set_default_response(1)

    if dialog.run() == 1:
      filename = dialog.get_filename()
      self.saveCollection(filename)

    dialog.destroy()

  def saveCollection(self, filename):
    self.savefile = filename
    file = open(filename, "w")
    file.write(self.database + "\n")

    for item in self.liststoreGames:
      if item[1] or item[2] or item[3]:
        save = item[0] + " ["
        if item[1]:
          save += "C"
        else:
          save += "-"
        if item[2]:
          save += "I"
        else:
          save += "-"
        if item[3]:
          save += "B"
        else:
          save += "-"
        file.write(save + "]\n")
    file.close()

  def clicked_open(self, menuitem):
    print "Open!"
    dialog = Gtk.FileChooserDialog("Open collection", menuitem.get_toplevel(), Gtk.FileChooserAction.OPEN)
    dialog.add_button(Gtk.STOCK_CANCEL, 0)
    dialog.add_button(Gtk.STOCK_OPEN, 1)
    dialog.set_default_response(1)

    #filefilter = Gtk.FileFilter()
    #filefilter.add_pixbuf_formats()
    #dialog.set_filter(filefilter)

    if dialog.run() == 1:
      filename = dialog.get_filename()
      self.savefile = filename

      file = open(filename, "r")
      self.newProject(file.readline().strip())
      for line in file:
        result = line.split(" [")
        for item in self.liststoreGames:
          if item[0] == result[0].strip():
            if result[1][0] == "C":
              item[1] = True
            if result[1][1] == "I":
              item[2] = True
            if result[1][2] == "B":
              item[3] = True
      file.close()

    dialog.destroy()
    self.updateStatus()

  def toggled_Cart(self, model, column):
    model[column][1] = not model[column][1]
    self.updateStatus()

  def toggled_Instructions(self, model, column):
    model[column][2] = not model[column][2]
    self.updateStatus()

  def toggled_Box(self, model, column):
    model[column][3] = not model[column][3]
    self.updateStatus()

  def updateStatus(self):
    ownedCarts = 0
    ownedInstructions = 0
    ownedBoxes = 0
    for item in self.liststoreGames:
      if item[1]:
        ownedCarts += 1
      if item[2]:
        ownedInstructions += 1
      if item[3]:
        ownedBoxes += 1

    ownedTotal = (float(ownedCarts + ownedInstructions + ownedBoxes) / (self.gameCount * 3)) * 100

    context_id = self.statusbar.get_context_id("Statusbar")
    self.statusbar.pop(self.statusid)
    self.statusid = self.statusbar.push(context_id, "Total collected: %.1f%% (Carts: %d/%d, Instructions: %d/%d, Boxes: %d/%d)" % (ownedTotal, ownedCarts, self.gameCount, ownedInstructions, self.gameCount, ownedBoxes, self.gameCount))


def main():
  app = Smscollector()
  Gtk.main()

if __name__ == '__main__':
  main()
