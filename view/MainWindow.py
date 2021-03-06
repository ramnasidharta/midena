import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSignal

from ui.fa_viewer import Ui_Dialog
from ui.main_window import Ui_MainWindow
from model.FiniteAutomata import FiniteAutomata
from utils import remove_flag


class MainWindow(QtWidgets.QMainWindow):

    faItemChanged = pyqtSignal(FiniteAutomata)
    faImport = pyqtSignal(str)
    faSave = pyqtSignal(str)
    faTestWord = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setTableItemFont()
        self.setupGrammarTable()

    def setTableItemFont(self):
        self.tableItemFont = QtGui.QFont()
        self.tableItemFont.setPointSize(18)
        self.tableItemFont.setWeight(50)

    def setupGrammarTable(self):
        self.ui.grammarTableWidget.setColumnCount(3)
        self.ui.grammarTableWidget.setRowCount(1)
        self.ui.grammarTableWidget.setHorizontalHeaderLabels(["α", "→", "ß"])
        self.addArrowToRow(self.ui.grammarTableWidget.currentRow() + 1)

    def addRowToGrammarTable(self):
        itemAlpha = QtWidgets.QTableWidgetItem()
        itemBeta = QtWidgets.QTableWidgetItem()
        itemAlpha.setFont(self.tableItemFont)
        itemBeta.setFont(self.tableItemFont)

        row = self.ui.grammarTableWidget.rowCount()
        self.ui.grammarTableWidget.setRowCount(row + 1)
        self.ui.grammarTableWidget.setItem(row + 1, 0, itemAlpha)
        self.ui.grammarTableWidget.setItem(row + 1, 2, itemBeta)
        self.addArrowToRow(row)

    def addArrowToRow(self, row):
        arrowItem = QtWidgets.QTableWidgetItem("   →")
        arrowItem.setFlags(QtCore.Qt.NoItemFlags)
        arrowItem.setFlags(QtCore.Qt.ItemIsEnabled)
        arrowItem.setFont(self.tableItemFont)

        self.ui.grammarTableWidget.setItem(row, 1, arrowItem)

    def addGrammarToListBox(self, g):
        self.ui.grammarsWidgetList.addItem(QtWidgets.QListWidgetItem(g.name))

    def clearGrammarFields(self):
        self.ui.initial_prod_textEdit.setText("")
        self.ui.symbols_textEdit.setText("")
        self.ui.terminals_textEdit.setText("")
        self.ui.grammar_name_textEdit.setText("")
        self.ui.grammarTableWidget.setRowCount(0)
        self.setupGrammarTable()

    def clearRegExField(self):
        self.ui.regExTextEdit.setText("")

    def add_listener(self, presenter):

        # Automatas
        self.ui.btn_create_fa.clicked.connect(self.onCreateFAClicked)
        self.ui.btn_import_fa.clicked.connect(self.onImportFAClicked)
        self.ui.btn_save_fa.clicked.connect(self.onSaveFAClicked)
        self.ui.btn_determinize_fa.clicked.connect(presenter.on_determinize_fa)
        self.ui.btn_minimize_fa.clicked.connect(presenter.on_minimize_fa)
        self.ui.btn_test_word.clicked.connect(self.on_test_word_clicked)
        self.faImport.connect(presenter.onImportFA)
        self.faSave.connect(presenter.on_save_fa)
        self.faItemChanged.connect(presenter.on_fa_item_changed)
        self.ui.convertFAtoRGBtn.clicked.connect(
            presenter.onConvertFAtoRGBtnClicked)

        self.ui.tableWidget.itemSelectionChanged.connect(
            self.on_fa_item_selected)
        self.ui.tableWidget.itemChanged.connect(self.on_fa_item_changed)

        # Grammars
        self.ui.btn_add_prod.clicked.connect(presenter.onAddProdClicked)
        self.ui.removeProductionBtn.clicked.connect(
            presenter.onRemoveProductionClicked)
        self.ui.btn_create_grammar.clicked.connect(
            presenter.onCreateGrammarClicked)
        self.ui.btn_remove_grammar.clicked.connect(
            presenter.on_remove_grammar_clicked)
        self.ui.exportGrammarBtn.clicked.connect(
            presenter.onExportGrammarBtnClicked)
        self.ui.importGrammarBtn.clicked.connect(
            presenter.onImportGrammarBtnClicked)
        self.ui.grammarToFABtn.clicked.connect(
            presenter.onGrammarToFABtnClicked)

        # Regular Expression
        self.ui.exportRegExBtn.clicked.connect(
            presenter.onExportRegExBtnClicked)
        self.ui.importRegExBtn.clicked.connect(
            presenter.onImportRegExBtnClicked)
        self.faTestWord.connect(presenter.on_test_word)

    def onCreateFAClicked(self):
        num_states, ok = QtWidgets.QInputDialog.getInt(
            self, "States", "Number of states:", 4, 1, 20, 1
        )
        if not ok:
            return

        num_sigma, okSigma = QtWidgets.QInputDialog.getInt(
            self, "Sigma", "Number of symbols:", 2, 1, 20, 1
        )
        if not okSigma:
            return

        sigma = [chr(i) for i in range(97, 97 + num_sigma)]
        table = {}
        for i in range(num_states):
            table['q' + str(i)] = {x: '-' for x in sigma}
        initial = 'q0'
        accepting = ['q' + str(num_states - 1)]
        self.current_fa = FiniteAutomata(sigma, table, initial, accepting)
        self.faItemChanged.emit(self.current_fa)

    def onImportFAClicked(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self)
        if path:
            self.faImport.emit(path)

    def onSaveFAClicked(self):
        if not self.current_fa:
            print("Error: No FA active")
            return

        path, _ = QtWidgets.QFileDialog.getSaveFileName(self)
        if path:
            self.faSave.emit(path)

    def showFA(self, fa: FiniteAutomata):
        self.ui.tableWidget.blockSignals(True)
        self.ui.tableWidget.clear()
        self.current_fa = fa
        sigma = {}
        for i, s in enumerate(sorted(fa.sigma), 1):
            sigma[i] = s

        states_label = {}
        for s in fa.states():
            label = s
            if (s in fa.accepting):
                label = '* ' + label
            if (s == fa.initial):
                label = '> ' + label
            states_label[s] = label

        # +2 para headers e adição de novos simbolos/estados
        cols = len(sigma) + 2
        rows = len(states_label) + 2
        self.ui.tableWidget.setColumnCount(cols)
        self.ui.tableWidget.setRowCount(rows)

        for i, state in enumerate(fa.states(), 1):
            self.ui.tableWidget.setItem(
                i, 0, QtWidgets.QTableWidgetItem(states_label[state])
            )
            for j, symbol in sigma.items():
                self.ui.tableWidget.setItem(
                    0, j, QtWidgets.QTableWidgetItem(symbol)
                )
                if symbol in fa.table[state]:
                    self.ui.tableWidget.setItem(
                        i, j, QtWidgets.QTableWidgetItem(
                            fa.transition_to_text(fa.table[state][symbol]))
                    )
        item = QtWidgets.QTableWidgetItem('')
        item.setFlags(remove_flag(item.flags(), Qt.ItemIsEnabled))
        self.ui.tableWidget.setItem(0, 0, item)

        item = QtWidgets.QTableWidgetItem('New Symbol')
        self.ui.tableWidget.setItem(0, cols - 1, item)
        item = QtWidgets.QTableWidgetItem('New State')
        self.ui.tableWidget.setItem(rows - 1, 0, item)
        for i in range(1, rows):
            item = QtWidgets.QTableWidgetItem('')
            item.setFlags(remove_flag(item.flags(), Qt.ItemIsEnabled))
            self.ui.tableWidget.setItem(i, cols - 1, item)
        for j in range(1, cols):
            item = QtWidgets.QTableWidgetItem('')
            item.setFlags(remove_flag(item.flags(), Qt.ItemIsEnabled))
            self.ui.tableWidget.setItem(rows - 1, j, item)
        self.ui.tableWidget.resizeColumnsToContents()
        self.ui.tableWidget.blockSignals(False)

    def showGrammar(self, g):
        self.ui.initial_prod_textEdit.setText(g.root)
        self.ui.symbols_textEdit.setText(",".join(list(g.symbols)))
        self.ui.terminals_textEdit.setText(",".join(list(g.sigma)))
        self.ui.grammar_name_textEdit.setText(g.name)
        self._showProductions(g.productions)

    def grammarToFA():
        ...

    def showRegEx(self, re):
        self.ui.regExTextEdit.setText(str(re))

    def _showProductions(self, productions):
        tableWidget = self.ui.grammarTableWidget
        tableWidget.setRowCount(0)
        row = 0
        for p in productions:

            # b = ["a", "B"] -> b = "aB"
            joinedBetas = list(map(lambda b: "".join(b), p[1]))
            alpha, betas = p[0], "|".join(joinedBetas)  # betas = b1|b2
            alphaItem = QtWidgets.QTableWidgetItem(alpha)
            betasItem = QtWidgets.QTableWidgetItem(betas)
            self.addRowToGrammarTable()
            tableWidget.setItem(row, 0, alphaItem)
            tableWidget.setItem(row, 2, betasItem)
            row += 1

    def column_to_symbol(self, column):
        return self.ui.tableWidget.item(0, column).text()

    def row_to_state(self, row):
        return self.ui.tableWidget.item(row, 0).text()

    def on_fa_item_selected(self):
        selected = self.ui.tableWidget.selectedItems()
        if selected:
            item = selected[0]
            self.fa_selected_item = item.text()

    def on_fa_item_changed(self, item):
        if item.row() == 0:
            # add or update sigma symbol
            symbol = item.text()
            if item.column() > len(self.current_fa.sigma):
                self.fa_selected_item = ''
            self.current_fa.update_sigma(self.fa_selected_item, symbol)
        elif item.column() == 0:
            # add or update state
            st = self.state_from_label(item.text())
            if item.row() > len(self.current_fa.states()):
                self.fa_selected_item = ''
            self.current_fa.update_state(
                self.state_from_label(self.fa_selected_item), st)
            if '*' in item.text():
                if st not in self.current_fa.accepting:
                    self.current_fa.accepting.append(st)
            else:
                if st in self.current_fa.accepting:
                    self.current_fa.accepting.remove(st)
            if '>' in item.text():
                self.current_fa.initial = st
        else:
            # add or update transition
            tr = item.text()
            st = self.state_from_label(self.row_to_state(item.row()))
            symbol = self.column_to_symbol(item.column())
            if tr == '':
                tr = '-'
            self.current_fa.table[st][symbol] = self.current_fa.text_to_transition(
                tr)
        self.ui.tableWidget.resizeColumnsToContents()
        self.faItemChanged.emit(self.current_fa)

    def state_from_label(self, label: str):
        return label.replace('>', '').replace('*', '').strip()

    def on_view_fa_clicked(self):
        from subprocess import call
        from PyQt5 import QtGui

        dialog = QtWidgets.QDialog()
        fa_ui = Ui_Dialog()
        fa_ui.setupUi(dialog)

        name = self.current_fa.name
        call(['/usr/bin/dot', '-Tpng', f'{name}.gv', '-o', f'{name}.png'])
        pixmap = QtGui.QPixmap(f'{name}.png')
        fa_ui.label.setPixmap(pixmap)
        fa_ui.label.setFixedSize(pixmap.size())
        fa_ui.label.show()

        dialog.exec_()

    def on_test_word_clicked(self):
        text = self.ui.edittext_test_word.text()
        self.faTestWord.emit(text)

    def show_test_word_msg(self, result):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setWindowTitle('Sentence Recognition')
        msgBox.setFixedWidth(400)
        msgBox.setText(f'Sentence is {result}.')
        msgBox.exec_()
