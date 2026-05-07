---
title: "Lombok"
type: entity
tags: [Java, 代码生成, 开源]
sources:
  - "[[摘要-idea-使用]]"
actionLink: "[[raw/09-archive/设计模式/raw/09-archive/Java学习/IDEA学习/Lombok 的使用]]"
last_updated: 2026-05-02
---

## 定义
Lombok 是一个 Java 库，通过注解自动生成 getter/setter/构造方法等样板代码，减少冗余。

## 常用注解
- **@Data**：包含 @Getter/@Setter/@ToString/@EqualsAndHashCode/@NoArgsConstructor
- **@Builder**：建造者模式
- **@Accessors(chain=true)**：链式编程
- **@Slf4j**：直接使用 log 对象
- **@Cleanup**：自动关闭资源
- **@RequiredArgsConstructor**：final 和 @NotNull 参数构造器

## 注意事项
- @Data + @AllArgsConstructor 会导致无参构造失效，需额外加 @NoArgsConstructor
- IDEA 需安装 lombok 插件
- 与 MapStruct 有编译冲突，需特殊处理

## 关联连接
- [[IntelliJ_IDEA]] — IDE 集成
- [[MapStruct]] — 编译冲突需注意
- [[摘要-idea-使用]] — 来源摘要
- [[raw/09-archive/设计模式/raw/09-archive/Java学习/IDEA学习/Lombok 的使用]] — 原始素材
