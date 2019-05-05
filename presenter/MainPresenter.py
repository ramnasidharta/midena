from PyQt5 import QtCore, QtGui, QtWidgets

from model.FileUtil import *
from model.RegularGrammar import RegularGrammar
from model.RegularExpression import RegularExpression
from presenter.UIObjectsCreator import *
from presenter.BasePresenter import BasePresenter


class MainPresenter(BasePresenter):

    def __init__(self, view):
        super().__init__(view)
        self.grammars = []

    def on_create_fa_clicked(self):
        pass

    def on_import_fa(self, path):
        self.current_fa = import_FA(path)
        self.view.show_FA(self.current_fa)

    def on_save_fa_clicked(self):
        if self.current_fa is not None:
            export_FA(self.current_fa, "tests/other_fa.json")

    def on_add_prod_clicked(self):
        self.view.addRowToGrammarTable()

    def onRemoveProductionClicked(self):
        n = self.view.ui.grammarTableWidget.rowCount()
        self.view.ui.grammarTableWidget.setRowCount(n-1)

    def onConvertFAtoRGBtnClicked(self):
        pass

    def on_create_grammar_clicked(self):
        s = self.view.ui.initial_prod_textEdit.toPlainText()
        symbols_entry = self.view.ui.symbols_textEdit.toPlainText()
        symbols = set(symbols_entry.split(','))
        terminals_entry = self.view.ui.terminals_textEdit.toPlainText()
        sigma = set(terminals_entry.split(','))
        name = self.view.ui.grammar_name_textEdit.toPlainText()

        grammar = None
        try:
            productions = read_productions(self.view.ui.grammarTableWidget)
            grammar = RegularGrammar(symbols, sigma, productions, s, name)
            self.view.addGrammarToListBox(grammar)
        except(ValueError):
            ...

        self.view.clearGrammarFields()
        self.grammars.append(grammar)
        return grammar

    def on_remove_grammar_clicked(self):
        selectedGrammar = self.view.ui.grammarsWidgetList.currentItem()
        row = self.view.ui.grammarsWidgetList.row(selectedGrammar)
        self.view.ui.grammarsWidgetList.takeItem(row)

    def onExportGrammarBtnClicked(self):
        selectedGrammar = self.view.ui.grammarsWidgetList.currentItem()
        if (selectedGrammar is not None):
            name = selectedGrammar.text()
            grammar = self.findByName(name)
            if grammar is not None:
                parent = self.view.ui.centralwidget
                fileName = promptFileName(parent, 'Export grammar to file',\
                        'Enter the file name:')
                exportGrammar(grammar, fileName)
        else:
            messageBox = QtWidgets.QMessageBox()
            messageBox.setText(
                    "Please, select in the list the grammar to be exported.")
            messageBox.exec_()

    def onImportGrammarBtnClicked(self):
        parent = self.view.ui.centralwidget
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(parent,\
                'Open file', "Midena Files (*.ext *.json)")
        if fileName != "":
            grammar = importGrammar(fileName)
            self.view.showGrammar(grammar)

    def onExportRegExBtnClicked(self):
        parent = self.view.ui.centralwidget
        fileName = promptFileName(parent, 'Export regular expression to file',\
                'Enter the file name:')

        regexStr = self.view.ui.regExTextEdit.toPlainText()
        # validate if regexStr is a valid regular expression with specific
        # automata (maybe in RegularExpression constructor)
        regex = RegularExpression(regexStr)
        exportRegEx(regex, fileName)
        self.view.clearRegExField()


    def onImportRegExBtnClicked(self):
        parent = self.view.ui.centralwidget
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(parent,\
                'Open file', "Midena Files (*.ext *.json)")
        if fileName != "":
            regex = importRegEx(fileName)
            self.view.showRegEx(regex)

    def findByName(self, name):
        for g in self.grammars:
            if g.name == name:
                return g
        return None

    def on_save_fa(self, path: str):
        if self.current_fa is not None:
            self.current_fa.name = path.split('/')[-1].replace('.json', '')
            export_FA(self.current_fa, path)

    def on_fa_item_changed(self, updated_fa):
        try:
            self.current_fa = updated_fa
            self.view.show_FA(updated_fa)
        except Exception as exc:
            print(f'Exception: {exc}')
