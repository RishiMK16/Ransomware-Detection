const express=require('express')
const {app,BrowserWindow}=require('electron')

const loadwindow=()=>{
    const win=new BrowserWindow({
        height:500,
        width:800
    });

    win.loadFile('index.html');
};


app.whenReady().then(()=>{
    loadwindow();
});


//to keep electron active even after all windows are terminated
app.on("window-all-closed",()=>{
    if(process.platform=="darwin")app.quit();
})