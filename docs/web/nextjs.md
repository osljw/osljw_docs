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


## mdx-bundler库

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


## @mdx-js/mdx


- compile, run, evaluate
  - https://mdxjs.com/guides/mdx-on-demand/  


```js
import { VFile } from 'vfile'
import { compile, nodeTypes, run } from '@mdx-js/mdx'
import { Fragment, jsx, jsxs } from 'react/jsx-runtime'

const runtime = { Fragment, jsx, jsxs }

const file = new VFile({
  basename: formatMarkdown ? 'example.md' : 'example.mdx',
  value,
})

// Compile MDX to JS.
await compile(file, {
  development: show === 'result' ? false : development,
  jsx: show === 'code' || show === 'esast' ? jsx : false,
  outputFormat: show === 'result' || outputFormatFunctionBody ? 'function-body' : 'program',
  recmaPlugins,
  rehypePlugins,
  remarkPlugins,
})

// Run code compiled with outputFormat: 'function-body'.
const mod = await run(String(file), {
  ...runtime,
  baseUrl: window.location.href,
})

return (
  <ErrorBoundary FallbackComponent={ErrorFallback} resetKeys={[value]}>
    <div className="playground-result">{mod.default({})}</div>
  </ErrorBoundary>
)
```

# FAQ

> app-index.js:32 Warning: Prop `id` did not match. Server: "tiny-react_56260481011700528269862" Client: "tiny-react_95895973821700528274024"


