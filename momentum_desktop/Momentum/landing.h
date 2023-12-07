#ifndef LANDING_H
#define LANDING_H

#include <QMainWindow>

QT_BEGIN_NAMESPACE
namespace Ui {
class Landing;
}
QT_END_NAMESPACE

class Landing : public QMainWindow
{
    Q_OBJECT

public:
    Landing(QWidget *parent = nullptr);
    ~Landing();

private:
    Ui::Landing *ui;
};
#endif // LANDING_H
