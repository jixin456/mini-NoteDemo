//index.js
//获取应用实例
const app = getApp()

Page({

  /**
   * 页面的初始数据
   */
  data: {
    //判断小程序的API,回调，参数，组件等是否在当前版本使用
    canIUse: wx.canIUse("button.open-type.getUserInfo"),
    url:"/images/my.png",
    hasUserInfo:false, 
    username:"游客"
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    //查看是否授权
    var that = this
    wx.getSetting({
      success: function (res) {
        if (res.authSetting["scope.userInfo"]) {
          wx.getUserInfo({
            success: function (res) {
              console.log(res.userInfo)
              console.log("hello")            
              //用户已经授权过
              if(app.globalData.userInfo){
                that.setData({
                  hasUserInfo:true,
                  url:app.globalData.userInfo.avatarUrl,
                  username:app.globalData.userInfo.nickName
                })
              }
            }
          })
        }
      }
    })
    // if(app.globalData.userInfo){
    //   this.setData({
    //     hasUserInfo:true,
    //     url:app.globalData.userInfo.avatarUrl,
    //     username:app.globalData.userInfo.nickName
    //   })
    // }
    
  },
  bindGetUserInfo:function(e){
    console.log("输出个人信息")
    console.log(e.detail.userInfo)
    if(e.detail.userInfo){
      //用户按了允许是授权按钮
      // app.login()//调取app.js的login（）方法进行注册
      app.globalData.userInfo = e.detail.userInfo
      app.login(e)//调取app.js的login（）方法进行注册
      
      this.setData({
        url:app.globalData.userInfo.avatarUrl,
        hasUserInfo:true,
        username: app.globalData.userInfo.nickName
      })
    }else{
      //用户拒绝了按钮
    }
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
