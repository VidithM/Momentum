#include <QApplication>
#include <QDir>
#include <QWebEngineView>
#include <QWebEngineSettings>

#include <iostream>
using std::cout;
using std::endl;

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);

    QWebEngineView webView;

    QString landingPath = "Assets/landing.html";
    QString currentDir = QDir::currentPath();
    QString fullPath = QDir(currentDir).filePath(landingPath);
    webView.page()->settings()->setAttribute(QWebEngineSettings::LocalContentCanAccessRemoteUrls, true);
    qDebug() << "[DBG] FULL PATH " << fullPath;
    QUrl localUrl = QUrl::fromLocalFile(fullPath);

    webView.setUrl(localUrl);
    webView.show();

    return a.exec();
}
