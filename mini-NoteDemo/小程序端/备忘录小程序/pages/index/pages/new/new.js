// pages/new/new.js
const app = getApp()
var accounts = app.globalData.note
var Request = require("../../utils/request.js")
var showToast = require("../../utils/showToast.js")
Page({

  /**
   * 页面的初始数据
   */
  data: {
    newItem: {
      id: "",
      content: ""
    }

  },
  //保存数据函数
  onSubmit: function (event) {
    //赋值content
    var item = this.data.newItem;
    item.content = event.detail.value.content;
    //赋值id
    // var accounts = app.globalData.note;
    console.log(accounts.length)
    item.id = String(accounts.length + 1);
    //赋值newItem
    this.setData({
      newItem: item
    });





    var data = {
      content:this.data.newItem.content
    }
    var url = "http://127.0.0.1:8000/note/upnote/"
    Request.request(url,data,"POST").then(function(Request){
      if(Request.statusCode == 200){
        showToast.showToast("发布成功","success")
      }
      if(Request.statusCode == 401){
        showToast.showToast("发布失败", "none")
        
      }

    },function(error){});





    //全局变量note增加上newItem数据
    app.globalData.note.push(this.data.newItem);
    //把新数据添加到首页来显示
    var pages = getCurrentPages()
    pages[pages.length - 2].setData({
      item: accounts
    })
    wx.showToast({
      title: '保存成功',
    });
    setTimeout(function () {
      wx.hideToast();
      wx.navigateBack({
      })
    }, 1000)
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  }
})