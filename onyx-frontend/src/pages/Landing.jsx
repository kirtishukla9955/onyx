import React from 'react';
import Navbar from '../components/Navbar';
import Hero from '../components/Hero';
import TrustStrip from '../components/TrustStrip';
import Features from '../components/Features';
import Pipeline from '../components/Pipeline';
import Proof from '../components/Proof';
import Pricing from '../components/Pricing';
import CTABanner from '../components/CTABanner';
import Footer from '../components/Footer';

export default function Landing() {
  return (
    <>
      <Navbar />
      <Hero />
      <TrustStrip />
      <Features />
      <Pipeline />
      <Proof />
      <Pricing />
      <CTABanner />
      <Footer />
    </>
  );
}
