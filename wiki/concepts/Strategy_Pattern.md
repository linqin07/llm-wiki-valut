---
title: "策略模式（Strategy Pattern）"
type: concept
tags: [设计模式, 行为型模式, Java, 算法封装, if-else优化]
sources:
  - raw/01-articles/设计模式/21.策略模式/
last_updated: 2026-05-01
---

## 定义

策略模式（Strategy Pattern）是一种行为型设计模式，定义一系列的算法，把它们一个个封装起来，并且使它们可相互替换。本模式使得算法可独立于使用它的客户而变化。

**意图**：定义算法族，封装每个算法。

**主要解决**：需要在运行时选择算法。

**何时使用**：在开发过程中，经常有这样的情况：`if elseif ... else`。条件少还好，一旦 `else if` 过多这里的逻辑将会比较混乱，并很容易出错。

**使用建议**：不要盲目使用，如果业务预测就几个分支，那么直接 `if else` 最好。当每个分支里面的操作都有一定的复杂时才有意义，不需要简单问题复杂化。

## 经典案例：计算机 USB 接口

电脑接口都支持 USB，通过 USB 可以连接鼠标、键盘、照相机等外接设备。

**USB 接口：**

```java
public interface USB {
    String readData(String data);
}
```

**实现类：**

```java
public class Camera implements USB {
    @Override
    public String readData(String data) {
        System.out.println("Camera");
        return data;
    }
}

public class Keyboard implements USB {
    @Override
    public String readData(String data) {
        System.out.println("Keyboard");
        return data;
    }
}

public class Mouse implements USB {
    @Override
    public String readData(String data) {
        System.out.println("Mouse");
        return data;
    }
}
```

**计算机类：**

```java
public class Computer {
    private USB usb;

    public void setUsb(USB usb) {
        this.usb = usb;
    }

    public String readData(String data) {
        return usb.readData(data);
    }
}
```

## 优化 if-else：使用枚举维护

**枚举类：**

```java
public enum UsbList {
    CAMERA("1", "照相机设备", "com.service.Camera"),
    KEYBOARD("2", "键盘设备", "com.service.Keyboard"),
    MOUSE("3", "鼠标设备", "com.service.Mouse");

    private String num;
    private String description;
    private String implClass;

    UsbList(String num, String description, String implClass) {
        this.num = num;
        this.description = description;
        this.implClass = implClass;
    }

    public static Map<String, Object> getAllClazz() {
        Map<String, Object> map = new HashMap<>();
        for (UsbList emum : UsbList.values()) {
            map.put(emum.getNum(), emum.getImplClass());
        }
        return map;
    }
}
```

**USB 选择器：**

```java
@Component
public class UsbSelector {
    public USB getInstance(String data) throws ClassNotFoundException {
        Map<String, Object> allClazz = UsbList.getAllClazz();
        String clazz = (String) allClazz.get(data);
        if (StringUtils.isEmpty(clazz)) {
            System.out.println("没有该实现类！");
        }
        USB usb = (USB) SpringBeanFactory.getBean(Class.forName(clazz));
        return usb;
    }
}
```

**控制器简化：**

```java
@RestController
public class TestController {
    @Autowired
    private Computer computer;

    @Autowired
    private UsbSelector usbSelector;

    @RequestMapping("/test")
    public String test(String data) throws ClassNotFoundException {
        USB instance = usbSelector.getInstance(data);
        computer.setUsb(instance);
        return computer.readData(data);
    }
}
```

## 优点

使用策略模式可以很好的对业务进行拓展，只需要增加一个接口实现就可以避免代码变得更加复杂。

## 应用场景

- 支付方式选择
- 排序算法切换
- 折扣计算
- 表单验证规则
- 替代复杂的 if-else 结构

## 关联连接

- [[Design_Patterns]] — 设计模式总览
- [[摘要-design-patterns-java]] — 来源摘要
- [[State_Pattern]] — 状态模式
- [[Template_Method_Pattern]] — 模板模式
- [[Factory_Pattern]] — 工厂模式
