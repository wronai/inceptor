/**
 * Termynal.js
 * A lightweight, modern and extensible animated terminal window, using
 * async/await.
 *
 * @author Inian Parameshwaran <inian1234@gmail.com>
 * @author Szymon Kaliski <szymon.kaliski@gmail.com>
 * @version 0.0.5
 * @license MIT
 */

'use strict';

/** Generate a terminal. */
class Termynal {
    /**
     * Initialize the terminal.
     * @param {string} selector - CSS selector of the terminal container.
     * @param {Object} options - Configuration options.
     * @param {string} options.prefix - Prefix to use for data attributes.
     * @param {number} options.startDelay - Delay before starting the animation (ms).
     * @param {number} options.typeDelay - Delay between each typed character (ms).
     * @param {number} options.lineDelay - Delay between each line (ms).
     * @param {string} options.progressLength - Number of characters displayed as progress bar.
     * @param {string} options.progressChar - Character to use for progress bar.
     * @param {number} options.progressPercent - Max percent of progress.
     * @param {string} options.cursor - Cursor character.
     * @param {string} options.lineData - Data attribute for line data.
     * @param {string} options.progressData - Data attribute for progress data.
     * @param {string} options.prompt - Data attribute for prompt data.
     */
    constructor(selector = '#termynal', options = {}) {
        this.terminal = document.querySelector(selector);
        this.pfx = `data-${options.prefix || 'ty'}`;
        this.startDelay = options.startDelay || 600;
        this.typeDelay = options.typeDelay || 90;
        this.lineDelay = options.lineDelay || 1500;
        this.progressLength = options.progressLength || 40;
        this.progressChar = options.progressChar || '█';
        this.progressPercent = options.progressPercent || 100;
        this.cursor = options.cursor || '▋';
        this.lineData = this.pfx + (options.lineData || 'line');
        this.progressData = this.pfx + (options.progressData || 'progress');
        this.prompt = this.pfx + (options.prompt || 'prompt');
        this.lines = [];
        this.started = false;
        this.currentLine = 0;
        
        // Initialize the terminal
        this.init();
    }

    /**
     * Initialize the terminal.
     */
    init() {
        if (!this.terminal) return;
        
        // Hide the terminal content until we start the animation
        this.terminal.setAttribute('data-termynal', '');
        this.terminal.style.visibility = 'hidden';
        
        // Process each line
        const lines = this.terminal.querySelectorAll(`[${this.lineData}]`);
        for (let line of lines) {
            const type = line.getAttribute(this.lineData);
            const prompt = line.getAttribute(this.prompt) || '';
            const progress = line.getAttribute(this.progressData);
            
            this.lines.push({
                element: line,
                type: type,
                prompt: prompt,
                progress: progress,
                chars: line.textContent
            });
            
            // Clear the line content
            line.textContent = '';
            line.style.visibility = 'hidden';
        }
        
        // Start the animation
        this.start();
    }
    
    /**
     * Start the animation.
     */
    start() {
        if (this.started) return;
        this.started = true;
        this.terminal.style.visibility = 'visible';
        
        // Start animating each line
        this.animateLine();
    }
    
    /**
     * Animate the current line.
     */
    async animateLine() {
        if (this.currentLine >= this.lines.length) {
            return;
        }
        
        const line = this.lines[this.currentLine];
        line.element.style.visibility = 'visible';
        
        // Add prompt if it exists
        if (line.prompt) {
            const prompt = document.createElement('span');
            prompt.className = 'terminal-prompt';
            prompt.textContent = line.prompt;
            line.element.appendChild(prompt);
        }
        
        // Handle different line types
        switch (line.type) {
            case 'input':
                await this.type(line);
                break;
                
            case 'progress':
                await this.progress(line);
                break;
                
            default:
                await this.type(line);
        }
        
        // Move to the next line
        this.currentLine++;
        if (this.currentLine < this.lines.length) {
            setTimeout(() => this.animateLine(), this.lineDelay);
        }
    }
    
    /**
     * Type out a line of text.
     * @param {Object} line - Line to type.
     */
    async type(line) {
        const chars = line.chars.split('');
        
        for (let i = 0; i < chars.length; i++) {
            await this.delay(this.typeDelay);
            line.element.textContent += chars[i];
        }
        
        // Add cursor if this is an input line
        if (line.type === 'input') {
            await this.delay(this.lineDelay);
            line.element.textContent = line.element.textContent.slice(0, -1);
        }
    }
    
    /**
     * Animate a progress bar.
     * @param {Object} line - Line with progress bar.
     */
    async progress(line) {
        const progressLength = line.progress || this.progressLength;
        const progressPercent = Math.min(parseInt(line.progress) || this.progressPercent, 100);
        const progressBar = document.createElement('span');
        
        line.element.appendChild(progressBar);
        
        for (let i = 1; i <= progressLength; i++) {
            await this.delay(this.typeDelay);
            const percent = Math.round((i / progressLength) * 100);
            progressBar.textContent = `[${this.progressChar.repeat(i)}${' '.repeat(progressLength - i)}] ${percent}%`;
            
            if (percent >= progressPercent) {
                break;
            }
        }
        
        await this.delay(this.lineDelay);
    }
    
    /**
     * Helper function to create a delay.
     * @param {number} time - Time to delay in milliseconds.
     */
    delay(time) {
        return new Promise(resolve => setTimeout(resolve, time));
    }
}

// Initialize all terminals on the page
document.addEventListener('DOMContentLoaded', () => {
    const terminals = document.querySelectorAll('[data-termynal]');
    terminals.forEach(terminal => {
        new Termynal(`#${terminal.id}`);
    });
});
