(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-bf546354"],{"138b":function(n,t,o){"use strict";o.r(t);var e=function(){var n=this,t=n.$createElement,o=n._self._c||t;return o("el-scrollbar",{staticClass:"page-component__scroll"},[o("el-carousel",{attrs:{interval:4e3,type:"card",height:"250px"}},n._l(n.carousel,(function(t){return o("el-carousel-item",{key:t},[o("el-image",{attrs:{src:n.imgHost+t+".png",fit:"contain"}})],1)})),1),o("el-card",{staticClass:"box-card"},[o("viewer",{attrs:{mainContent:n.blogInfo}})],1),o("el-backtop",{attrs:{target:".page-component__scroll .el-scrollbar__wrap",right:20}})],1)},a=[],s=o("e099"),r=o("00b7"),i={name:"blog",components:{viewer:r["a"]},data:function(){return{imgHost:s["a"].QiNiuHost,blogInfo:s["a"].blogInfo,carousel:["python","golang","gnu","ubuntu","kernel","root","sudo","vim"]}},methods:{},mounted:function(){}},l=i,c=(o("333b"),o("9ca4")),u=Object(c["a"])(l,e,a,!1,null,"f8cc14ca",null);t["default"]=u.exports},"333b":function(n,t,o){"use strict";var e=o("3e84"),a=o.n(e);a.a},"3e84":function(n,t,o){},e099:function(n,t,o){"use strict";var e="http://qiniu.messstack.com/",a="#### 关于博客\n\n搭建blog在我开始编程时，便放在了计划之中，但是困于自己能力不足，而心比天高，还有就是生活所迫。拖延至今天才勉强将 blog的基本框架搭完。\n\n今后的日志我将慢慢的增加功能并优化目前这个blog项目，使之好看且使用。同时记录自己作为一个码农，在开发过程中遇到的困难与解决的思路、笔记和好用的工具推荐等等\n\n本项目已经挂在github上，如果有兴趣的小伙伴可以一起优化，感激不尽。\n\n项目地址：[后端项目地址](https://github.com/zengxiaolou/blog-back)、[前端项目地址](https://github.com/zengxiaolou/blog-front)\n\n#### 本项目用到的技术栈\n\n**前端：**Vue2.0框架，运用vue-cli4作为脚手架快速完成前端项目主体搭建\n\n- Vue组件：Vue-router、Vuex、Axios\n- UI库：ElementUI\n- 第三方库：Echarts、ToastUI-Editor\n\n**后端：**\n\n- 语言：python\n- 框架：基础框架Django(3.0)， API快速开发框架Django-Restful-Framework\n- 主要第三方包：JWT、Rest_Captcha、Social_Django、Celery、drf_yasg、qiniu、Requests\n\n**数据库：**\n\n- Mysql、Redis、Elstiacsearch\n\n**部署：**\n\n- Docker-Compose、Nginx\n\n#### 项目更新记录 \n\n2020年10月01 \n\n  前端版本：版本V1.0.0\n\n  后端版本：版本V1.0.0\n\n\n\n#### 博客文章涉及范围\n\n博主是个会计毕业，野路子出来的程序员，目前在一家小公司上班。近几年所学比较杂，而且没有好好的系统学习过编程，但是对编程充满兴趣。所以文章涉及的东西相对比较杂乱，有兴趣的小伙伴可以相互探讨进步；文章将按以下分组归类：\n\n- Python  本渣目前最熟悉的语言\n- Vue    本渣目前接触最多的前端框架、感觉很好用\n- Go     最感兴趣的语言，虽然最近几年炒的比较热，但生态仍不是很完善，要靠有兴趣的小伙伴加油了\n- Linux   主要分享linux相关的知识与技术，我目前只知道个大概，但是作为一个程序员，为了避免curd，linux还是要好好学习\n- Docker 目前最火的容器技术，虽然是便运维的技术，但是作为一个开发，还是需要弄懂，在开发中会事半功倍，后面估计会取了解K8S\n- DB    目前熟悉的有 关系型数据库：Mysql、Sqlite3、PostgreSQL；非关系型数据库： Redis、MongoDB、Elasticsearch\n- Tools   主要是分享自己开发过程中，认为比较好的工具，能提高开发效率的\n- Other  这个分类暂定是分享一些与开发不太相关的文章、开始做算法题之后，估计会新增一算法分类\n\n#### 功能简介\n\n目前博客功能较少，后续会根据需求增加；\n\n- 已有功能：\n\n- - 用户登录\n  - 文章展示\n  - 文章点赞与二级评论\n  - 文章归档与文章日历热力图\n  - 关于博客\n  - 站内搜索\n  - 个人简介\n  - 创作中心\n  - 社交直达\n  - 标签与分类\n\n- 计划功能：\n\n- - 网站数据统计（图表）\n  - Tui-Editor图片上传改为直接上传到七牛云\n  - 用户中心\n  - 动态菜单\n  - 评论点赞功能，根据点赞排序\n";t["a"]={QiNiuHost:e,blogInfo:a}}}]);