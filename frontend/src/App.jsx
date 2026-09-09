import dellLogo from "./assets/dell-logo.svg";
import "./App.css";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

if (!API_BASE_URL) {
    throw new Error("Не задана переменная VITE_API_BASE_URL");
}

const OFFER = "Dell";

const categories = [
    {
        number: "01",
        title: "Work & study",
        description:
            "Explore laptops for everyday tasks, learning, and staying connected.",
    },
    {
        number: "02",
        title: "Create & explore",
        description:
            "Find a computer for your next idea, creative project, or personal workspace.",
    },
    {
        number: "03",
        title: "Build your setup",
        description:
            "Discover desktops, monitors, and accessories for a space that works for you.",
    },
];

/**
 * @param {string} placement
 * @returns {string}
 */
function createClickUrl(placement) {
    const url = new URL("/click", API_BASE_URL);

    // URLSearchParams кодирует значения параметров.
    url.searchParams.set("offer", OFFER);
    url.searchParams.set("sub1", placement);

    return url.toString();
}

/**
 * @param {{
 *   placement: string,
 *   children: import("react").ReactNode,
 *   secondary?: boolean
 * }} props
 * @returns {import("react").ReactElement}
 */
function CtaLink({ placement, children, secondary = false }) {
    return (
        <a
            className={secondary ? "button button-secondary" : "button"}
            href={createClickUrl(placement)}
            data-cta-id={placement}
            data-offer={OFFER}
        >
            {children}
        </a>
    );
}

/**
 * @returns {import("react").ReactElement}
 */
function App() {
    return (
        <>
            <a className="skip-link" href="#main">
                Skip to content
            </a>

            <header className="site-header">
                <div className="container header-content">
                    <img
                        className="brand-logo"
                        src={dellLogo}
                        alt="Dell"
                        width={56}
                        height={56}
                    />
                    <span className="header-note">Independent brand guide</span>
                </div>
            </header>

            <main id="main">
                <section className="hero">
                    <div className="container hero-layout">
                        <div className="hero-content">
                            <p className="eyebrow">Work. Create. Connect.</p>

                            <h1>Make room for your next big idea.</h1>

                            <p className="hero-description">
                                Discover Dell laptops, desktops, and
                                accessories. Explore the possibilities and find
                                your next setup on the official Dell website.
                            </p>

                            <CtaLink placement="hero">Explore Dell</CtaLink>

                            <p className="link-note">
                                Continue to the official Dell website
                            </p>
                        </div>

                        <div className="hero-art" aria-hidden="true">
                            <div className="art-orbit" />
                            <div className="art-window">
                                <div className="art-toolbar">
                                    <span />
                                    <span />
                                    <span />
                                </div>
                                <div className="art-screen">
                                    <span>Your next chapter.</span>
                                </div>
                            </div>
                            <span className="art-caption">
                                A fresh perspective starts here.
                            </span>
                        </div>
                    </div>
                </section>

                <section className="categories section">
                    <div className="container">
                        <p className="eyebrow">Find your direction</p>
                        <h2>A setup for what matters to you.</h2>

                        <div className="category-grid">
                            {categories.map((category) => (
                                <article
                                    className="category-card"
                                    key={category.number}
                                >
                                    <span className="category-number">
                                        {category.number}
                                    </span>
                                    <h3>{category.title}</h3>
                                    <p>{category.description}</p>
                                </article>
                            ))}
                        </div>

                        <div className="section-action">
                            <CtaLink placement="categories" secondary>
                                Discover the range
                            </CtaLink>
                        </div>
                    </div>
                </section>

                <section className="section">
                    <div className="container">
                        <div className="closing-panel">
                            <div>
                                <p className="eyebrow">Take the next step</p>
                                <h2>Explore your options with Dell.</h2>
                                <p>
                                    Check current products, specifications,
                                    pricing, and availability directly on the
                                    official website.
                                </p>
                            </div>

                            <CtaLink placement="footer">Visit Dell</CtaLink>
                        </div>
                    </div>
                </section>
            </main>

            <footer className="site-footer">
                <div className="container">
                    <p>
                        Educational demo. This page is not an official Dell
                        website and is not affiliated with Dell. Dell trademarks
                        belong to their respective owners.
                    </p>
                </div>
            </footer>
        </>
    );
}

export default App;
