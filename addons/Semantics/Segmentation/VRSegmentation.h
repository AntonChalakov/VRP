#ifndef VRSEGMENTATION_H_INCLUDED
#define VRSEGMENTATION_H_INCLUDED

#include <OpenSG/OSGConfig.h>
#include <OpenSG/OSGVector.h>
#include <vector>
#include <map>

#include "core/objects/VRObjectFwd.h"

OSG_BEGIN_NAMESPACE;
using namespace std;

enum SEGMENTATION_ALGORITHM {
    HOUGH = 0
};

struct Vertex;
struct Edge;
struct Triangle;
struct Border;

struct Edge {
    vector<Vertex*> vertices;
    vector<Triangle*> triangles;
    Border* border = 0;
    bool isBorder = false;

    Edge();
    Vertex* other(Vertex* v);
    Triangle* other(Triangle* t);
    vector<Edge*> borderNeighbors();
    Vec3f segment();
    Vertex* vertexTo(Edge* e);
    bool isLinked(Edge* e);
    bool has(Vertex* v);
};

struct Vertex {
    vector<Edge*> edges;
    vector<Triangle*> triangles;
    Border* border = 0;
    bool isBorder = false;
    Vec3f v;
    Vec3f n;
    int ID;

    Vertex(Pnt3f p, Vec3f n, int i);
    vector<Vertex*> neighbors();
    vector<Vertex*> borderNeighbors();
};

struct Triangle {
    vector<Vertex*> vertices;
    vector<Edge*> edges;
    Border* border = 0;

    Triangle();
    void addEdges(map<int, Edge*>& Edges);
    void addVertices(Vertex* v1, Vertex* v2, Vertex* v3);
    Edge* getOtherEdge(Edge* e, Vertex* v);
};

struct Border {
    vector<Vertex*> vertices;

    void add(Vertex* v, bool prepend = false);
};


class VRSegmentation {
    private:
        VRSegmentation();

    public:

        static VRObjectPtr extractPatches(VRGeometryPtr geo, SEGMENTATION_ALGORITHM algo, float curvature, float curvature_delta, Vec3f normal, Vec3f normal_delta);
        static vector<int> growPatch(VRGeometryPtr geo, int i);

        static void removeDuplicates(VRGeometryPtr geo);
        static void fillHoles(VRGeometryPtr geo, int steps);

        static VRObjectPtr convexDecompose(VRGeometryPtr geo);
};

OSG_END_NAMESPACE;

#endif // VRSEGMENTATION_H_INCLUDED
