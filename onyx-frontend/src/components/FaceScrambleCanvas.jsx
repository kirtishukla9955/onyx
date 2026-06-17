import React, { useRef, useEffect } from 'react';

// Signature visual: a face-node mesh that continuously scrambles/reassembles,
// dramatizing the "Digital Camouflage" adversarial perturbation concept.
export default function FaceScrambleCanvas() {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    let width, height, dpr;
    let raf;
    let t = 0;

    // Face-ish node layout: an oval cloud of points denser at center,
    // loosely suggesting facial landmark positions.
    const NODE_COUNT = 140;
    let nodes = [];

    function resize() {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      const rect = canvas.parentElement.getBoundingClientRect();
      width = rect.width;
      height = rect.height;
      canvas.width = width * dpr;
      canvas.height = height * dpr;
      canvas.style.width = width + 'px';
      canvas.style.height = height + 'px';
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      buildNodes();
    }

    function buildNodes() {
      nodes = [];
      const cx = width / 2;
      const cy = height / 2;
      const rx = width * 0.30;
      const ry = height * 0.36;

      for (let i = 0; i < NODE_COUNT; i++) {
        const angle = Math.random() * Math.PI * 2;
        const r = Math.pow(Math.random(), 0.55);
        const baseX = cx + Math.cos(angle) * rx * r;
        const baseY = cy + Math.sin(angle) * ry * r;
        nodes.push({
          baseX, baseY,
          x: baseX, y: baseY,
          offsetSeed: Math.random() * 1000,
          scrambleSeed: Math.random() * 1000,
          size: Math.random() * 1.6 + 0.6,
          isAnchor: Math.random() > 0.82
        });
      }
    }

    function draw() {
      ctx.clearRect(0, 0, width, height);
      t += 1;

      const cycle = (Math.sin(t * 0.004) + 1) / 2; // 0 -> 1 -> 0 breathing scramble amount
      const scrambleAmt = cycle * 38;

      // update positions
      nodes.forEach((n) => {
        const nx = Math.sin(t * 0.01 + n.scrambleSeed) * scrambleAmt;
        const ny = Math.cos(t * 0.013 + n.scrambleSeed * 1.3) * scrambleAmt;
        const driftX = Math.sin(t * 0.006 + n.offsetSeed) * 2.2;
        const driftY = Math.cos(t * 0.007 + n.offsetSeed) * 2.2;
        n.x = n.baseX + nx + driftX;
        n.y = n.baseY + ny + driftY;
      });

      // draw connecting lines between near nodes
      ctx.lineWidth = 0.6;
      for (let i = 0; i < nodes.length; i++) {
        for (let j = i + 1; j < nodes.length; j++) {
          const a = nodes[i], b = nodes[j];
          const dx = a.x - b.x, dy = a.y - b.y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < 46) {
            const alpha = (1 - dist / 46) * 0.22 * (1 - cycle * 0.6);
            ctx.strokeStyle = `rgba(0, 240, 255, ${alpha})`;
            ctx.beginPath();
            ctx.moveTo(a.x, a.y);
            ctx.lineTo(b.x, b.y);
            ctx.stroke();
          }
        }
      }

      // draw nodes
      nodes.forEach((n) => {
        const glowAlpha = n.isAnchor ? 0.95 : 0.55;
        const color = n.isAnchor ? '0, 240, 255' : '160, 230, 255';
        ctx.beginPath();
        ctx.arc(n.x, n.y, n.size + (n.isAnchor ? 0.6 : 0), 0, Math.PI * 2);
        ctx.fillStyle = `rgba(${color}, ${glowAlpha})`;
        ctx.shadowBlur = n.isAnchor ? 8 : 3;
        ctx.shadowColor = 'rgba(0,240,255,0.8)';
        ctx.fill();
      });
      ctx.shadowBlur = 0;

      raf = requestAnimationFrame(draw);
    }

    resize();
    draw();
    window.addEventListener('resize', resize);
    return () => {
      window.removeEventListener('resize', resize);
      cancelAnimationFrame(raf);
    };
  }, []);

  return (
    <div className="relative w-full h-full">
      <canvas ref={canvasRef} className="w-full h-full" />
    </div>
  );
}
