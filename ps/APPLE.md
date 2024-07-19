
# Apple, PostScript, PDF and screen rendering

As can be read from the background of [PostScript](POSTSCRIPT.md), in the
mid 80s Apple had a great success early with the event of "affordable"
laser printers, programs where you could layout pictures, text and graphics
such as PageMaker, but also PostScript which could transfer what you saw on
the screen to what got printed in relatively high detail as 300 dpi.

PostScript produced crisp, scalable fonts (not easy to copy) and detailed graphics,
crucial for required clear, readable text and precise illustrations. This ensured
that printed materials looked excellent regardless of the printer used:
*device-independent*.

Apple’s LaserWriter printer, one of the first to incorporate PostScript, played
a key role. Combined with the Macintosh’s *graphical user interface*, it allowed
seamless production, blending text and graphics smoothly.

Using PostScript was part of Apple’s larger initiative in the *desktop publishing
revolution* (DTP). Along with software like Aldus PageMaker, it enabled users to
create professional-quality documents in-house, showcasing the capabilities of the
Macintosh in producing high-quality printed materials.

PostScript allowed to consistently documents to be reproduced at any size and
on any compatible printer without losing quality. This was beneficial for
producing various editions and updates, maintaining high standards across
all copies.

WYSIWYG (What You See Is What You Get) as PostScript maintained the fidelity of
on-screen displays to printed outputs, allowing users to see exactly how the
printed manual would look, ensuring accuracy and detail.

Macintosh didn't make a great start when it launched. But DTP and some other
software made it into a much more attractive product in crucial markets,
at the right time.


## PDF renders PostScript a bit obsolete ..

Much later on PostScript was succeeded by PDF (Portable Document Format),
to which it can easily be "distilled", or converted.
PDF actually inherits much of ideas from PostScript, although the format
has changed a lot. It has a different focus, which makes it suitable
for not only printers but also screens.[^pdf]

But here comes the interesting part: *PDF played a significant role in
screen rendering and display within Apple's operating systems, particularly
starting from Mac OS X, which arrived in 2001.*

[^pdf]: https://en.wikipedia.org/wiki/PDF


### Historical Context

- **PostScript to PDF Transition**: While PostScript was integral to the
early days of desktop publishing and printing, PDF emerged as a more versatile
and portable format for document exchange and display. Adobe developed PDF
to extend the capabilities of PostScript, making it better suited for a range
of devices and platforms, including on-screen viewing. In fact PDF wasn't
an immediate success at all when it lauched in the early 90s. The success
it has today took a long time to arrive at.

- **PDF as a Universal Format**: As PDF became the de facto standard for
*document exchange*, its use in on-screen rendering became more prevalent.
Apple's adoption of PDF for its rendering engine in macOS leveraged the
strengths of PDF, providing a unified approach to rendering that worked
equally well for on-screen display, printing, and document exchange.


### PDF in Apple's GUI

**Core Graphics (Quartz 2D)**: Apple's Core Graphics framework, known as Quartz 2D,
is the cornerstone of their graphics rendering engine in macOS. Quartz 2D is based
on the same imaging model as *PDF*. This allows the operating system to render text
and graphics with high precision and consistency, using the same techniques for
both screen display and printing.

**Resolution Independence**: PDF's scalable nature means that graphics and text can
be rendered at (for the most part) any resolution without loss of quality. This was
a critical feature for Apple's GUI, ensuring that elements would look sharp and clear
on displays with varying resolutions, including the high-resolution Retina displays
introduced later.

**Consistent Output**: Using PDF as a basis for on-screen rendering ensures that the
visual output is consistent across different devices. This is similar to the WYSIWYG
(What You See Is What You Get) principle that PostScript brought to desktop publishing.
What users see on their screen is a faithful representation of what will be printed
or displayed on another device.

**Advanced Graphics Features**: PDF supports advanced graphics features such as
transparency, gradients, and complex vector shapes. By utilizing PDF for rendering,
Apple's GUI could incorporate these advanced graphics features seamlessly, enhancing
the visual appeal and functionality of the user interface.

**Performance Optimization**: Apple's implementation of PDF for rendering is optimized
for performance, ensuring smooth and responsive interactions within the GUI. The
efficient handling of vector graphics and text rendering helps maintain a high frame
rate and responsiveness, even with complex visuals.

**Compatibility and Integration**: PDF is a widely used standard for document exchange,
and by using it as a basis for their rendering engine, Apple ensured that documents
created or viewed on macOS would be highly compatible with other systems and applications.
This integration makes it easier for users to work with PDF documents directly within
the operating system, including previewing, annotating, and printing.



## Going Metal ..

As of recent developments, Apple has indeed evolved its graphics rendering
 architecture, moving away from a strictly PDF-based approach for certain
 aspects of screen buffering and rendering. Here’s an overview of the current
 situation and how Apple’s graphics architecture has shifted:

### Changes and Evolution

1. **Metal Framework**:
    - **Introduction**: Apple introduced Metal, a low-level, high-performance
    graphics API, in 2014 with iOS 8 and later expanded it to macOS. Metal
    provides direct access to the GPU, allowing for more efficient rendering
    and greater control over graphics performance.
    - **Use Cases**: Metal is used extensively for rendering complex graphics
    and animations in games, professional applications, and system-level
    rendering tasks where high performance is critical.
    - **Screen Rendering**: For many modern applications, especially those
    requiring intensive graphics, Metal is used instead of traditional PDF-based
    rendering.

2. **Core Animation and Core Graphics**:
    - **Core Animation**: Core Animation remains a fundamental part of macOS and iOS for managing animations and smooth transitions. It interfaces with both Metal and Core Graphics to provide high-performance, visually appealing animations.
    - **Core Graphics (Quartz 2D)**: While still integral for many 2D rendering tasks, Core Graphics now often works in conjunction with Metal for improved performance and flexibility. The use of PDF for certain tasks persists, but it is not the sole method for all rendering operations.

3. **Hybrid Approach**:
    - **PDF for Document Rendering**: PDF is still heavily used for document rendering and manipulation within macOS and iOS. Apps that handle documents, such as Preview and third-party PDF viewers, leverage the PDF capabilities of Core Graphics for accurate rendering and editing.
    - **Metal for Performance-Critical Tasks**: For tasks that require high performance, such as real-time graphics, complex UI elements, and advanced animations, Metal is preferred due to its efficiency and direct access to GPU resources.

4. **Layered Architecture**:
    - **UI Rendering**: The UIKit and AppKit frameworks (for iOS and macOS, respectively) utilize a layered rendering architecture where higher-level abstractions may still use PDF-based rendering internally, but lower-level operations are often offloaded to Metal for performance.
    - **Compositing and Effects**: Compositing and visual effects are areas where Metal’s capabilities are leveraged to provide smooth and efficient rendering, particularly on high-resolution displays and in graphics-intensive applications.

### Current Situation

- **Performance Optimization**: The shift towards using Metal reflects Apple’s focus on optimizing performance, particularly for applications that require real-time graphics and complex visual effects.
- **Consistency and Compatibility**: Despite these changes, Apple ensures that the visual output remains consistent and compatible with existing standards, including PDF. This is crucial for applications dealing with document rendering and ensures a seamless user experience.
- **Developer Tools**: Apple continues to provide robust developer tools and frameworks that allow developers to take advantage of both PDF-based rendering for document-centric applications and Metal for performance-intensive tasks.

### Summary

While Apple has not completely abandoned PDF-based rendering, especially for document handling and certain UI elements, it has significantly expanded its graphics architecture to incorporate Metal for high-performance rendering tasks. This hybrid approach allows Apple to maintain the strengths of PDF for certain applications while leveraging the advanced capabilities of Metal for tasks that demand higher performance and efficiency. The result is a more flexible and powerful rendering infrastructure that can cater to a wide range of application needs.


### Metal API

**Purpose**: Metal is a low-level graphics API designed for high-performance rendering and computation. It provides direct access to the GPU, allowing developers to achieve maximum efficiency and control over rendering tasks.

#### Features:
1. **Low-Level Access**: Metal provides direct access to the GPU, enabling developers to write highly optimized code for rendering and computation tasks.
2. **High Performance**: Metal is designed for performance-critical applications, such as games, professional graphics software, and real-time rendering.
3. **Compute Shaders**: Besides graphics rendering, Metal supports general-purpose computing on the GPU, which can be used for tasks like image processing and machine learning.
4. **Explicit Control**: Developers have explicit control over resource management, rendering pipelines, and synchronization, allowing for fine-tuned performance optimizations.


### PDF Rendering (Core Graphics/Quartz 2D)

**Purpose**: Core Graphics (also known as Quartz 2D) is a 2D graphics
rendering API designed for drawing and rendering vector graphics,
including PDF content. It is well-suited for applications involving
document rendering, vector graphics, and text rendering.

#### Features:
1. **High-Level Drawing**: Core Graphics provides high-level functions
for drawing shapes, text, and images.
2. **PDF Support**: Built-in support for rendering PDF documents,
including page navigation and content extraction.
3. **Vector Graphics**: Ideal for drawing resolution-independent
vector graphics.
4. **Integration with UIKit/AppKit**: Seamless integration with
higher-level frameworks for UI rendering.



### Differences in API Usage

- **Level of Abstraction**: Metal provides a lower-level API with more explicit control over rendering operations and resource management, while Core Graphics offers a higher-level, more abstracted API focused on ease of use for 2D graphics and PDF rendering.
- **Performance and Use Cases**: Metal is designed for high-performance, real-time applications requiring direct GPU access. In contrast, Core Graphics is tailored for applications involving vector graphics and document rendering, where ease of use and integration with the system’s UI framework are more important.
- **Resource Management**: Metal requires explicit management of GPU resources, synchronization, and command encoding, whereas Core Graphics handles many of these aspects automatically, providing a simpler but less flexible drawing model.


### Conclusion
Metal and Core Graphics serve different purposes within Apple's graphics architecture. Metal is aimed at performance-intensive tasks requiring fine control over the GPU, while Core Graphics focuses on high-level 2D graphics and PDF rendering. Developers choose between these APIs based on the specific needs of their applications, leveraging Metal for real-time graphics and Core Graphics for document-centric tasks.