# make_image  
每日制作云主机的OS镜像 
确保有人改了环境或者代码能及时回滚回去 
 
#功能： 
1、遍历所有地区 
2、遍历所有项目 
3、支持过滤 
4、支持删除x天前的镜像 
 
 
使用步骤： 
1、填写 
public_key = "xxxxxxxxx"   
private_key = "xxxxxxx"  

2、配置好python环境后，运行 

3、del_3day_images.py是配套脚本，删除3天以前的镜像。 效果如下：  
![Image text](https://github.com/lious68/make_image/blob/main/d02e36bf-a08a-476d-9a20-219ce309cd59.jpeg)
