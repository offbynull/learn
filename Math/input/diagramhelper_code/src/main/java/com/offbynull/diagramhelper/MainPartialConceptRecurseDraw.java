package com.offbynull.diagramhelper;

import static com.google.common.base.Throwables.getStackTraceAsString;
import com.google.common.hash.Hashing;
import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Desktop;
import java.awt.Dimension;
import java.awt.geom.Arc2D;
import java.io.File;
import java.io.IOException;
import java.io.Writer;
import static java.nio.charset.StandardCharsets.UTF_8;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Set;
import org.apache.batik.dom.GenericDOMImplementation;
import org.apache.batik.svggen.SVGGeneratorContext;
import org.apache.batik.svggen.SVGGraphics2D;
import org.w3c.dom.DOMImplementation;
import org.w3c.dom.Document;

public final class MainPartialConceptRecurseDraw {

    public static void main(String[] args) throws IOException {
        try (Writer mdOut = Files.newBufferedWriter(Path.of("/output/output.md"), UTF_8)) {
            try {
                String input = Files.readString(Path.of("/input/input.data"), UTF_8).trim();

                DOMImplementation domImpl = GenericDOMImplementation.getDOMImplementation();
                Document document = domImpl.createDocument("http://www.w3.org/2000/svg", "svg", null);

                int width = 500;
                int height = 500;

                SVGGraphics2D g = new SVGGraphics2D(SVGGeneratorContext.createDefault(document), true);
                g.setSVGCanvasSize(new Dimension(width, height));
                g.setStroke(new BasicStroke(0.2f));

                int[] digits = input.chars().map(i -> i - '0').toArray();
                drawSlices(g, width, height, digits, 9, true);

                String outputFileName = MainPartialConceptRecurseDraw.class.getSimpleName()
                        + Hashing.goodFastHash(32).hashString(input, UTF_8).toString() + ".svg";
                try (Writer writer = Files.newBufferedWriter(Path.of("/output", outputFileName))) {
                    g.stream(writer, false);
                }
                mdOut.write("![Concept diagram for partial rule " + input + "](" + outputFileName + ")");
            } catch (Exception e) {
                mdOut.append("`{bm-linker-off}`\n\n");
                mdOut.append(getStackTraceAsString(e));
                mdOut.append("`{bm-linker-on}`");
            }
        }
    }
    
    public static void drawSlices(SVGGraphics2D g, double width, double height, int[] digits, int maxDigit) {
        drawSlices(g, width, height, digits, maxDigit, false);
    }
    
    public static void drawSlices(SVGGraphics2D g, double width, double height, int[] digits, int maxDigit, boolean drawEmpty) {
        int limit = maxDigit + 1;
        double degreeOffset = 0;
        double degreesPerSlice = 360 / limit;
        for (int digit : digits) {
            drawSlices(g, width, height, digit, drawEmpty ? limit : digit, degreesPerSlice, degreeOffset);
            degreeOffset += degreesPerSlice * digit;
            degreesPerSlice = degreesPerSlice / limit;
        }
    }
    
    public static void drawSlices(SVGGraphics2D g, double width, double height, int fillSlices, int maxSlices, double degreesPerSlice, double degreeOffset) {
        g.setPaint(Color.gray);
        for (int i = 0; i < fillSlices; i++) {
            g.fill(
                    new Arc2D.Double(
                            0,
                            0,
                            width,
                            height,
                            degreeOffset + (i * degreesPerSlice),
                            degreesPerSlice,
                            Arc2D.PIE
                    )
            );
        }
        g.setPaint(Color.white);
        for (int i = fillSlices; i < maxSlices; i++) {
            g.fill(
                    new Arc2D.Double(
                            0,
                            0,
                            width,
                            height,
                            degreeOffset + (i * degreesPerSlice),
                            degreesPerSlice,
                            Arc2D.PIE
                    )
            );
        }
        g.setPaint(Color.black);
        for (int i = 0; i < maxSlices; i++) {
            g.draw(
                    new Arc2D.Double(
                            0,
                            0,
                            width,
                            height,
                            degreeOffset + (i * degreesPerSlice),
                            degreesPerSlice,
                            Arc2D.PIE
                    )
            );
        }
    }
}