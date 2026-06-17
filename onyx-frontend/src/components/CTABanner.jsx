import React from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';

export default function CTABanner() {
  return (
    <section className="relative py-24 px-6 lg:px-10">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, scale: 0.97 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="relative gradient-border rounded-3xl bg-void-panel px-8 py-16 lg:py-20 text-center overflow-hidden"
        >
          <div className="absolute inset-0 grid-bg opacity-30" />
          <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[700px] h-[400px] spotlight" />
          <div className="relative">
            <h2 className="font-display font-semibold text-4xl lg:text-5xl leading-tight max-w-2xl mx-auto">
              Your next deepfake target is already <span className="text-cyan-glow text-glow-cyan">scraping right now.</span>
            </h2>
            <p className="text-ink-dim text-lg mt-5 max-w-xl mx-auto">
              Cloak your next upload in under sixty seconds. No watermark you can see, no clone they can use.
            </p>
            <Link
              to="/signup"
              className="shine group inline-flex items-center gap-2 mt-9 px-8 py-4 rounded-full bg-cyan-glow text-void-deep font-semibold hover:shadow-[0_0_36px_rgba(0,240,255,0.55)] transition-shadow"
            >
              Activate Identity Shield
              <ArrowRight size={18} className="group-hover:translate-x-1 transition-transform" />
            </Link>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
