package com.offbynull.factor;

import static com.google.common.base.Throwables.getStackTraceAsString;
import com.google.common.hash.Hashing;
import java.awt.FontMetrics;
import java.awt.geom.Line2D;
import java.awt.geom.NoninvertibleTransformException;
import java.awt.geom.Rectangle2D;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.Writer;
import static java.nio.charset.StandardCharsets.UTF_8;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashSet;
import java.util.Scanner;
import java.util.Set;
import org.apache.batik.anim.dom.SAXSVGDocumentFactory;
import org.apache.batik.bridge.BridgeContext;
import org.apache.batik.bridge.DocumentLoader;
import org.apache.batik.bridge.GVTBuilder;
import org.apache.batik.bridge.UserAgent;
import org.apache.batik.bridge.UserAgentAdapter;
import org.apache.batik.dom.GenericDOMImplementation;
import org.apache.batik.gvt.GraphicsNode;
import org.apache.batik.svggen.SVGGeneratorContext;
import org.apache.batik.svggen.SVGGraphics2D;
import org.apache.batik.util.XMLResourceDescriptor;
import org.w3c.dom.*;

public class FactorTree {
    public static void main(String[] args) throws IOException {
        try (Writer mdOut = Files.newBufferedWriter(Path.of("/output/output.md"), UTF_8)) {
            try {
                String input = Files.readString(Path.of("/input/input.data"), UTF_8).trim();
                
                Scanner scanner = new Scanner(input);
                
                int testNum = scanner.nextInt();
                
                Node node = factorTree(testNum);

                DOMImplementation domImpl = GenericDOMImplementation.getDOMImplementation();
                Document document = domImpl.createDocument("http://www.w3.org/2000/svg", "svg", null);

                SVGGraphics2D g = new SVGGraphics2D(SVGGeneratorContext.createDefault(document), true);

                drawBranch(g, 0, 0, node);

                String outputFileName = FactorTree.class.getSimpleName()
                        + Hashing.murmur3_128(32).hashString(input, UTF_8).toString() + ".svg";
                writeSvg(g, Path.of("/output", outputFileName));
                mdOut.write("![Factore tree diagram for " + input + "](" + outputFileName + ")");
            } catch (Exception e) {
                mdOut.append("`{bm-disable-all}`\n\n");
                mdOut.append(getStackTraceAsString(e));
                mdOut.append("`{bm-enable-all}`");
            }
        }
    }
    
    //MARKDOWN_ISOLATE
    private static final Node factorTree(int input) {
        Set<FactorPair> factorPairs = getFactorPairs(input);
        
        // remove factor pairs [1, input] and/or [input, 1], then pick a factor
        FactorPair factorPair = factorPairs.stream()
                .filter(fp -> fp.factor1 != 1 && fp.factor2 != 1)
                .findFirst().orElse(null);
        
        if (factorPair == null) {
            Node node = new Node();
            node.value = input;
            node.left = null;
            node.right = null;
            return node;
        } else {
            Node node = new Node();
            node.value = input;
            node.left = factorTree(factorPair.factor1);
            node.right = factorTree(factorPair.factor2);
            return node;
        }
    }
    //MARKDOWN_ISOLATE
    
    private static final class Node {
        private int value;
        private Node left;
        private Node right;
    }
    
    private static final Set<FactorPair> getFactorPairs(int input) {
        Set<FactorPair> factorPairs = new HashSet<>();
        for (int factor1 = 1; factor1 <= input; factor1++) {
            int factor2 = input / factor1;
            boolean divHadRemainder = input % factor1 > 0;
            if (!divHadRemainder) {
                factorPairs.add(new FactorPair(factor1, factor2));
            }
            if (factor2 <= factor1) {
                break;
            }
        }
        return factorPairs;
    }
    
    private static final class FactorPair {
        private final int factor1;
        private final int factor2;

        public FactorPair(int factor1, int factor2) {
            this.factor1 = factor1;
            this.factor2 = factor2;
        }

        @Override
        public int hashCode() {
            int hash = 3;
            hash = 37 * hash + this.factor1;
            hash = 37 * hash + this.factor2;
            return hash;
        }

        @Override
        public boolean equals(Object obj) {
            if (this == obj) {
                return true;
            }
            if (obj == null) {
                return false;
            }
            if (getClass() != obj.getClass()) {
                return false;
            }
            final FactorPair other = (FactorPair) obj;
            if (this.factor1 != other.factor1) {
                return false;
            }
            if (this.factor2 != other.factor2) {
                return false;
            }
            return true;
        }

        @Override
        public String toString() {
            return factor1 + "/" + factor2;
        }
        
    }
    









    private static final double BRANCH_DIST = 50;

    private static void drawBranch(SVGGraphics2D g, double x, double y, Node node) throws NoninvertibleTransformException {
        FontMetrics fm = g.getFontMetrics();
        
        String str = node.value + "";
        
        double width = fm.stringWidth(str);
        double height = fm.getHeight();
        
        g.drawString(str, (float) (x - width / 2), (float) (y + height));
        
        if (node.left != null) {
            double startX = x;
            double startY = y + height;
            double nextX = x - BRANCH_DIST;
            double nextY = y + BRANCH_DIST;
            g.draw(new Line2D.Double(startX, startY, nextX, nextY));
            drawBranch(g, nextX, nextY, node.left);
        }
        if (node.right != null) {
            double startX = x;
            double startY = y + height;
            double nextX = x + BRANCH_DIST;
            double nextY = y + BRANCH_DIST;
            g.draw(new Line2D.Double(startX, startY, nextX, nextY));
            drawBranch(g, nextX, nextY, node.right);
        }
    }

    private static void writeSvg(SVGGraphics2D g, Path path) throws IOException {
        // after any invocation to stream() or any dom accessor (including this method), g's contents will clear and you'll need to reset it
          // see https://issues.apache.org/jira/browse/BATIK-555
          // see http://batik.2283329.n4.nabble.com/How-to-set-viewbox-attribute-in-SVGGraphics2D-td2979195.html
        Element tlgElement = g.getTopLevelGroup();
        g.setTopLevelGroup(tlgElement);
        
        // write out
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        OutputStreamWriter writer = new OutputStreamWriter(baos, UTF_8);
        g.stream(writer, false);
        g.setTopLevelGroup(tlgElement); // bug work around, see above
        
        // load back up and get svg bounds
        SAXSVGDocumentFactory factory = new SAXSVGDocumentFactory(XMLResourceDescriptor.getXMLParserClassName());
        Document document = factory.createDocument(
                null,
                new ByteArrayInputStream(baos.toByteArray())
        );
        UserAgent userAgent = new UserAgentAdapter();
        DocumentLoader documentLoader = new DocumentLoader(userAgent);
        BridgeContext bridgeContext = new BridgeContext(userAgent, documentLoader);
        bridgeContext.setDynamic(true);
        GraphicsNode graphicsNode = new GVTBuilder().build(bridgeContext, document);
        Rectangle2D bounds = graphicsNode.getSensitiveBounds();

        
        // pull out element to set viewport and bounds (dont use g.setSVGCanvasSize because it requires ints instead of doubles) and write out
        Element root = g.getRoot();
        root.setAttributeNS(null, "viewBox", bounds.getMinX() + " " + bounds.getMinY() + " " + bounds.getWidth()+ " " + bounds.getHeight());
        root.setAttributeNS(null, "width",  "" + bounds.getWidth());
        root.setAttributeNS(null, "height", "" + bounds.getHeight());
        try (Writer fileWriter = Files.newBufferedWriter(path)) {
            g.stream(root, fileWriter, false, false); // stream out the root element specifically -- g is cleared so if we stream it out directly it'll be blank
        }
        g.setTopLevelGroup(tlgElement); // bug work around, see above
    }
}
