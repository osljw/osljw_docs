
# qt



# QGraphicsView QGraphicsScene QGraphicsItem QGraphicsItemGroup

```
MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow),
    gscene( new QGraphicsScene()),
    gview( new QGraphicsView ()),
    resizeItem( new QGraphicsItemGroupResize())
{
    ui->setupUi(this);

    gscene->addItem(resizeItem);
    gview->setScene(gscene);
    gview->setParent(this);
    gview->show();
}

MainWindow::~MainWindow()
{
    delete resizeItem;
    delete gscene;
    delete gview;
    delete ui;
}
```
注意析构顺序

QGraphicsItem 拖拽

# QWidget
位置
- this->pos()  
This property holds the position of the widget within its parent widget

- this->move()
move接受的坐标是相对于parent widget

键盘事件
- 键盘事件没有被parent widget拦截
- this->setFocusPolicy(Qt::StrongFocus);

# 拖拽 drag

```
mousePressEvent - 记录鼠标起始位置
mouseMoveEvent - 计算鼠标偏移量，用偏移量更新位置
mouseReleaseEvent - 
```

# 全屏切换
full screen时没有stylesheet， normal时存在stylesheet
- showNormal()
- showFullScreen()

调用这两个函数之前先设置stylesheet，margin，如果之后在设置，会导致child QWidget的resize被再次调用。
