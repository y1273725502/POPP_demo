
def read(self):
    print("��ѡ��nuccore_result.txt")
    fold, _ = QFileDialog.getOpenFileName(self.ui, "ѡ��nuccore_result.txt")
    print(fold)
    filter_mitochondrial.filter_mitochondrial(fold)