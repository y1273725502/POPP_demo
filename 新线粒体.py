
def read(self):
    print("«Î—°‘Ònuccore_result.txt")
    fold, _ = QFileDialog.getOpenFileName(self.ui, "—°‘Ònuccore_result.txt")
    print(fold)
    filter_mitochondrial.filter_mitochondrial(fold)