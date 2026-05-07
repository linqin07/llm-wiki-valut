# Wiki 操作日志

## [2026-05-01] ingest | 引入 Spring Boot 知识库

- **变更**: 新增实体 [[Spring_Boot]], [[GraphQL]], [[MyBatis]], [[MyBatis_Plus]], [[Druid]], [[Swagger]], [[Thymeleaf]], [[Spring_Security]], [[WebSocket]], [[JPA]], [[MapStruct]], [[Redis]]; 新增概念 [[spring-boot-auto-configuration]], [[spring-boot-aop]], [[spring-boot-exception-handler]], [[spring-boot-interceptor]], [[spring-boot-json]], [[spring-boot-logback]], [[spring-boot-scheduled-tasks]], [[spring-boot-deployment]], [[spring-boot-multi-environment]]; 新增来源摘要 [[摘要-spring-boot-知识库]]; 更新 [[index.md]]
- **冲突**: 无

## [2026-05-01] ingest | 引入 MySQL 知识体系

- **变更**: 新增实体 [[MySQL]], [[InnoDB]], [[MyISAM]], [[Oracle]]; 新增概念 [[ACID事务]], [[MVCC]], [[B+树索引]], [[redo-log]], [[undo-log]], [[binlog]], [[数据库隔离级别]], [[SQL优化]], [[分库分表]]; 新增来源摘要 7 篇; 更新 [[index.md]]
- **冲突**: 无

## [2026-05-01] ingest | 引入 Spring Cloud 微服务体系

- **变更**: 新增实体 [[Eureka]], [[Nacos]], [[Spring_Cloud_Gateway]], [[Zuul]], [[Feign]]; 新增概念 [[服务注册中心]], [[服务网关]], [[CAP定理]]; 新增来源摘要 [[摘要-spring-cloud-微服务]]; 更新 [[index.md]]
- **冲突**: 无

---

## [2026-05-02] query | 检索 Spring Boot 核心知识
- **输出**: 即时回答未保存（用户未确认）
- **引用页面**: [[Spring_Boot]], [[spring-boot-auto-configuration]], [[spring-boot-multi-environment]], [[spring-boot-aop]], [[MyBatis]], [[Redis]], [[Spring_Security]]

---

## [2026-05-02] ingest | 批量引入 raw/ 全部待处理文件（~140篇）

- **变更**:
  - Java学习（~40篇）: 新增实体 [[Arthas]], [[Git]], [[GitLab]], [[IntelliJ_IDEA]], [[Lombok]], [[Tomcat]], [[Netty]], [[Akka]], [[SkyWalking]], [[Jenkins]], [[JHipster]], [[Maven]], [[Nexus]], [[Guava]], [[OkHttp3]], [[JVM]]; 新增概念 [[Stream-API]], [[函数式编程]], [[JVM调优]], [[synchronized锁]], [[泛型]], [[SPI机制]], [[正则表达式]]; 新增来源摘要 13 篇
  - Linux（~50篇）: 新增实体 [[Docker]], [[Elasticsearch]], [[Kafka]], [[ZooKeeper]], [[Nginx]], [[MongoDB]]; 更新 [[Redis]]（合并集群/缓存/分布式锁知识）; 新增来源摘要 10 篇
  - Spring（~10篇）: 新增来源摘要 [[摘要-spring-mvc-实践]], [[摘要-spring-技术点]]
  - 大模型应用开发（2篇）: 新增来源摘要 [[摘要-llm-应用开发]]
  - 数据结构（3篇）: 新增来源摘要 [[摘要-数据结构]]
  - 复习题（~15篇）: 新增来源摘要 [[摘要-java-复习题]]
  - 更新 [[index.md]] 新增 6 个分类板块
- **冲突**: 无
- **跳过**: raw/09-archive/ 已归档文件未处理; README/SUMMARY/book.json 结构性文件未单独生成页面

## [2026-05-02] lint | 知识库健康巡检与修复

- **变更**:
  - 移除 index.md 死链: [[Chain_of_Responsibility_Pattern]]（文件不存在）
  - 同步 3 个未注册页面到 index.md: [[Prompt_Engineering]], [[摘要-spring-mvc-实践]], [[摘要-spring-技术点]]
  - 清理 27 个内容死链（目标页面不存在的 [[双链]] 转为纯文本）
  - 为 18 个弱关联页面补充交叉引用（从相关实体页面添加反向链接）
- **结果**: 死链归零，孤儿页面从 19 降至 1（[[摘要-python-环境配置]] 无 Python 实体页可引用）
- **冲突**: 无

## [2026-05-07] sync | 全局知识图谱关联修复

- **变更**:
  - **Phase 1+2**: 修复 134 个页面的 sources 路径（`raw/01-articles/` → `raw/09-archive/`），为每个页面添加原始素材双链到 `## 关联连接` 部分
  - **Phase 3**: 新建 [[Chain_of_Responsibility_Pattern]] 页面并注册到 index.md; 删除 [[Druid]] 的无效 actionLink; 修复 5 个幽灵来源引用（Akka/SPI机制/Guava/JVM调优）
  - **Phase 4**: 为 19 个弱关联页面补充反向链接，主要增强 Spring_Boot/Eureka/Nacos/Spring_Cloud_Gateway 等枢纽页面的出链
  - **Phase 5**: 修复 [[摘要-python-环境配置]] 孤儿页面（添加到 Prompt_Engineering）; 修复剩余幽灵引用（JVM/Nexus/OkHttp3/Tomcat/Thymeleaf/ZooKeeper 等）
- **结果**: 死链归零，sources 路径全部有效，所有页面均与原始素材建立双链关联
- **已知问题**: Prompt_Engineering.md 的 2 个 sources 路径（Gemini API/Anthropic）对应文件未归档到 raw/09-archive/

## [2026-05-07] sync | 全局关联修复与 frontmatter 规范化

- **变更**:
  - 为全部 135 个 wiki 页面添加 `actionLink` 属性（双链回 raw/ 原始素材）
  - 将所有 `sources` 字段从 raw 路径格式转换为 `[[wikilink]]` 格式
  - 截断超过 3 个 sources 的文件，末尾加注释说明
  - 为 22 个设计模式文件填充 `sources: [[摘要-design-patterns-java]]`
  - 增强 Oracle、泛型、正则表达式、SPI机制、synchronized锁、MongoDB 等文件的关联连接
- **覆盖**: 135/135 文件完成 actionLink，0 文件使用旧格式 sources
- **冲突**: 无

## [2026-05-07] sync | 设计模式文件夹重命名与引用更新

- **变更**: 移除 `raw/09-archive/设计模式/` 下 23 个子文件夹的数字前缀（如 `1.单例模式` → `单例模式`），同步更新 wiki 中 401 处双链引用
- **冲突**: 无
