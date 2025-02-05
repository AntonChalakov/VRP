#include "VRGraphLayout.h"
#include "core/math/Octree.h"

using namespace OSG;

VRGraphLayout::VRGraphLayout() {}

VRGraphLayoutPtr VRGraphLayout::create() { return VRGraphLayoutPtr( new VRGraphLayout() ); }

void VRGraphLayout::setGraph(GraphPtr g) { graph = g; }
GraphPtr VRGraphLayout::getGraph() { return graph; }
void VRGraphLayout::setAlgorithm(ALGORITHM a, int p) { algorithms[p] = a; }
void VRGraphLayout::clearAlgorithms() { algorithms.clear(); }
void VRGraphLayout::setAlgorithm(string a, int p) {
    ALGORITHM A = SPRINGS;
    if (a == "OCCUPANCYMAP") A = OCCUPANCYMAP;
    setAlgorithm(A, p);
}

void VRGraphLayout::applySprings(float eps, float v) {
    if (!graph) return;
    for (auto& n : graph->getEdges()) {
        for (auto& e : n) {
            auto f1 = getFlag(e.from);
            auto f2 = getFlag(e.to);
            if (f1 & INACTIVE || f2 & INACTIVE) continue;

            auto& n1 = graph->getNode(e.from);
            auto& n2 = graph->getNode(e.to);
            Vec3f p1 = n1.box.center();
            Vec3f p2 = n2.box.center();

            float r = radius + n1.box.radius() + n2.box.radius();
            Vec3f d = p2 - p1;
            float x = d.length() - r; // displacement
            d.normalize();
            if (abs(x) < eps) continue;

            p1 += d*x*v;
            p2 += -d*x*v;
            auto po1 = graph->getPosition(e.from);
            auto po2 = graph->getPosition(e.to);
            po1->setPos(p1);
            po2->setPos(p2);
            switch (e.connection) {
                case Graph::SIMPLE:
                    if (!(f1 & FIXED)) graph->setPosition(e.from, po1);
                    if (!(f2 & FIXED)) graph->setPosition(e.to, po2);
                    break;
                case Graph::HIERARCHY:
                    if (!(f2 & FIXED)) graph->setPosition(e.to, po2);
                    else if (!(f1 & FIXED)) graph->setPosition(e.from, po1);
                    break;
                case Graph::DEPENDENCY:
                    if (!(f1 & FIXED)) graph->setPosition(e.from, po1);
                    else if (!(f2 & FIXED)) graph->setPosition(e.to, po2);
                    break;
                case Graph::SIBLING:
                    if (x < 0) { // push away siblings
                        if (!(f1 & FIXED)) graph->setPosition(e.from, po1);
                        if (!(f2 & FIXED)) graph->setPosition(e.to, po2);
                    }
                    break;
            }
        }
    }
}

void VRGraphLayout::applyOccupancy(float eps, float v) {
    if (!graph) return;
    auto& nodes = graph->getNodes();
    Octree o(10*eps);

    for (unsigned long i=0; i<nodes.size(); i++) {
        if ( isFlag(i, INACTIVE) ) continue;
        auto& n = nodes[i];
        o.addBox( n.box, (void*)i );
    }

    for (uint i=0; i<nodes.size(); i++) {
        if ( isFlag(i, FIXED) || isFlag(i, INACTIVE) ) continue;
        auto& n = nodes[i];
        Vec3f pn = n.box.center();

        Vec3f D;
        for (auto& on2 : o.boxSearch(n.box) ) {
            uint j = (long)on2;
            if (i == j) continue; // no self interaction

            auto& n2 = nodes[j];
            Vec3f d = n2.box.center() - pn;
            Vec3f w = n.box.size() + n2.box.size();

            Vec3f vx = Vec3f(abs(d[0]), abs(d[1]), abs(d[2])) - w*0.5;
            float x = vx[0]; // get smallest intrusion
            if (abs(vx[1]) < abs(x) && w[1] > 0) x = vx[1];
            if (abs(vx[2]) < abs(x) && w[2] > 0) x = vx[2];

            //cout << " dir " << dir << "   x " << x << "   d " << d << "   w2 " << w*0.5 << "   vx " << vx << endl;
            //cout << "displ " << i << " " << j << " w " << n.box.size() << " + " << n2.box.size() << "    d " << d << "    x " << x << endl;
            if (abs(x) < eps) continue;
            d.normalize();
            D -= d*abs(x);
        }

        auto po = graph->getPosition(i);
        po->setPos(pn+v*D);
        graph->setPosition(i, po); // move node away from neighbors
    }
}

void VRGraphLayout::compute(int N, float eps) {
    if (!graph) return;
    for (int i=0; i<N; i++) { // steps
        for (auto a : algorithms) {
            switch(a.second) {
                case SPRINGS:
                    applySprings(eps, 0.03);
                    break;
                case OCCUPANCYMAP:
                    applyOccupancy(eps, 0.5);
                    break;
            }
        }
    }

    // update graph nodes a second time
    for (uint i=0; i<graph->getNodes().size(); i++) graph->update(i, false);
}

void VRGraphLayout::setFlag(int i, FLAG f) {
    if (!flags.count(i)) flags[i] = NONE;
    flags[i] = flags[i] | f;
}

void VRGraphLayout::remFlag(int i, FLAG f) {
    if (!flags.count(i)) flags[i] = NONE;
    if ((f & flags[i]) == f) {
        flags[i] = flags[i] & ~f;
    }
}

bool VRGraphLayout::isFlag(int i, FLAG f) {
    if (!flags.count(i)) flags[i] = NONE;
    return (f & flags[i]);
}

int VRGraphLayout::getFlag(int i) { return flags.count(i) ? flags[i] : NONE; }
void VRGraphLayout::fixNode(int i) { setFlag(i, FIXED); }
void VRGraphLayout::setNodeState(int i, bool s) { if(!s) setFlag(i, INACTIVE); else remFlag(i, INACTIVE); }

void VRGraphLayout::setRadius(float r) { radius = r; }
void VRGraphLayout::setSpeed(float s) { speed = s; }
void VRGraphLayout::setGravity(Vec3f v) { gravity = v; }

void VRGraphLayout::clear() {
    flags.clear();
}


