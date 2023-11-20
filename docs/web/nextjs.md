# nextjs



 `src/pages/_app.js`: 自定义APP

`postcss.config.js`: https://www.tailwindcss.cn/docs/installation/using-postcss


# nextjs 


layout

https://blog.logrocket.com/guide-next-js-layouts-nested-layouts/



## app router

- layout
  - shared between multiple pages
  - On navigation, layouts preserve state, remain interactive, and do not re-render.

  - Layouts are Server Components by default but can be set to a Client Component.

- page
  -  unique to a route

## 编译 部署

```
next build
```


 # MDX


mdx-bundler库

`bundleMDX`: 从文本source生成code, frontmatter,  bundleMDX运行在服务器端，负责将mdx文件或内容编译打包为code， code是string类型，包含组件打包代码

`getMDXComponent`:  从code得到React组件

 ```js
import { ComponentMap, getMDXComponent } from 'mdx-bundler/client'

const Wrapper: React.ComponentType<{ layout: string }> = ({ layout, ...rest }) => {
  const Layout = require(`../layouts/${layout}`).default
  return <Layout {...rest} />
}

export const MDXComponents: ComponentMap = {
  Image,
  Video,
  //@ts-ignore
  TOCInline,
  a: CustomLink,
  pre: Pre,
  wrapper: Wrapper,
  //@ts-ignore
  BlogNewsletterForm,
}

export const MDXLayoutRenderer = ({ layout, mdxSource, ...rest }: Props) => {
  const MDXLayout = useMemo(() => getMDXComponent(mdxSource), [mdxSource])

  return <MDXLayout layout={layout} components={MDXComponents} {...rest} />
}
```

wrapper 使用自定义组件后， 可以根据文章中的layout，动态使用文章中指定的组件进行渲染

``` js
export default function BlogPost({ code, frontmatter }) {
    const Component = useMemo(() => getMDXComponent(code), [code]);

    return (
    <>
        <h1>{frontmatter.title}</h1>
        <p>{frontmatter.description}</p>
        <p>{frontmatter.date}</p>
        <article>
            <Component
                componets={{
                PostImage,
                InternalAnchor,
                PostRecommender,
                }}
            />
        </article>
    <>
    )
}
```


## mdx-bundler 教程
https://www.peterlunch.com/blog/mdx-bundler-beginners
