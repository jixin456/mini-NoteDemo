//app.js
App({
  onLaunch: function() {
    //调用API从本地缓存中获取数据
    var jwt = wx.getStorageSync('jwt');
    var that = this;
    if (!jwt) {
      //检查 jwt 是否存在 如果不存在调用登录
      console.log("1")
      //jwt不存在调用login()函数
      that.login()
    } else {
      console.log("2")
      //jsw存在
      this.globalData.jwt = jwt
    }
  },

  login: function (e) {
    var userinfo = e
    // 登录部分代码
    var that = this;
    wx.login({
      // 调用 login 获取 code
      success: function (res) {
        var code = res.code;
        console.log(code)
        console.log("login()获取code成功")
        try {
          that.globalData.userInfo = userinfo.detail.userInfo;
          var encryptedData = userinfo.detail.encryptedData || 'encry';
          var iv = userinfo.detail.iv || 'iv';
        } catch (e) {
          console.log("userInfo为null")
          return false
        }
        wx.request({ // 发送请求 获取 jwt
          url: "http://127.0.0.1:8000/users/login/",
          header: {
            Authorization: 'JWT' + that.globalData.access_token,
          },
          data: {
            username: encryptedData,
            password: iv,
            code: code,
          },
          method: "POST",
          success: function (res) {
            if (res.statusCode === 200) {
              // 得到 jwt 后存储到 storage，
              console.log(res.data.token)
              wx.showToast({
                title: '登录成功',
                icon: 'success'
              });
              wx.setStorage({
                key: "jwt",
                data: res.data.token
              });
              that.globalData = res.data
              that.globalData.jwt = res.data.token
              that.globalData.access_token = res.data.token;
              that.globalData.account_id = res.data.sub;
            } else if (res.statusCode === 400) {
              // 如果没有注册调用注册接口
              console.log("调用register()函数")
              that.register(userinfo);
            } else {
              // 提示错误信息
              wx.showToast({
                title: res.data.text,
                icon: 'success',
                duration: 2000
              });
            }
          },
          fail: function (res) { }
        })
      }
    })

  },
  register: function (e) {
    // 注册代码
    var that = this;
    var userinfo = e
    wx.login({ // 调用登录接口获取 code
      success: function (res) {
        console.log("register()时获取code成功")
        var code = res.code;
        try {
          that.globalData.userInfo = userinfo.detail.userInfo;
          var encryptedData = userinfo.detail.encryptedData || 'encry';
          var iv = userinfo.detail.iv || 'iv';
        } catch (e) {
          console.log('shibai')
          return false
        }
        wx.request({ // 请求注册用户接口
          url: "http://127.0.0.1:8000/users/Registered/",
          header: {
            // Authorization: config.basic_token
          },
          data: {
            username: encryptedData,
            password: iv,
            code: code,
          },
          method: "POST",
          success: function (res) {
            if (res.statusCode == 201) {
              console.log("@@@")
              that.login(userinfo);
            }
            if (res.statusCode == 401) {
              console.log("!!!")              
              that.register(userinfo);
            }
          },
          fail: function (res) { 
            console.log("?????")
          }
        })

      }
    })

  },
  globalData: {
    userInfo: null,
    jwt:null,
    note: [{
        id: '1',
        content: '我们都知道，Django是一种基于Python的Web开发框架。',
      },
      {
        id: '2',
        content: '那么，什么是Web开发？Web开发指的是开发基于B/S架构，通过前后端的配合，将后台服务器的数据在浏览器上展现给前台用户的应用',
      },
      {
        id: '3',
        content: '比如将电子购物网站的商品数据在浏览器上展示给客户，在基于浏览器的学校系统管理平台上管理学生的数据，监控机房服务器的状态并将结果以图形化的形式展现出来等等。',
      },
      {
        id: '4',
        content: '使用Python开发Web应用，最简单、原始和直接的办法是使用CGI标准，在二十年前这种方式很流行。它是如何做的呢？ ',
      },
      {
        id: '5',
        content: '服务过程是这样的：首先，用户请求CGI，脚本代码打印Content-Type行等一些HTML的起始标签，然后连接数据库并执行一些查询操作，获取最新的十件商品的相关数据',
      },
      {
        id: '6',
        content: '在遍历这些商品的同时，生成一个商品的HTML列表项，然后输出HTML的结束标签并且关闭数据库连接',
      },
      {
        id: '7',
        content: '如果应用中有多处需要连接数据库会怎样呢？每个独立的CGI脚本，不应该重复编写数据库连接相关的代码。',
      },
      {
        id: '8',
        content: '如果代码被重用到一个复合的环境中会发生什么？',
      },
    ],
  }
})