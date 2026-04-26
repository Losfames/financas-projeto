(function () {
    function injectStyles() {
        if (document.getElementById('site-modal-styles')) {
            return;
        }

        const style = document.createElement('style');
        style.id = 'site-modal-styles';
        style.textContent = `
            .site-modal-backdrop {
                position: fixed;
                inset: 0;
                z-index: 9999;
                display: none;
                align-items: center;
                justify-content: center;
                padding: 16px;
                background: rgba(0, 0, 0, 0.45);
            }

            .site-modal-backdrop.is-open {
                display: flex;
            }

            .site-modal-box {
                width: min(100%, 430px);
                border-radius: 8px;
                background: #F2F0EF;
                box-shadow: 0 24px 60px rgba(0, 0, 0, 0.28);
                overflow: hidden;
                font-family: Arial, sans-serif;
            }

            .site-modal-header {
                border-bottom: 1px solid rgba(40, 94, 158, 0.18);
                padding: 18px 20px 12px;
            }

            .site-modal-brand {
                margin: 0 0 8px;
                font-size: 18px;
                font-weight: 700;
                line-height: 1;
            }

            .site-modal-brand-green {
                color: #68A535;
            }

            .site-modal-brand-blue {
                color: #285E9E;
            }

            .site-modal-title {
                margin: 0;
                color: #285E9E;
                font-size: 20px;
                font-weight: 700;
            }

            .site-modal-message {
                margin: 0;
                padding: 18px 20px;
                color: #333333;
                font-size: 15px;
                line-height: 1.5;
                white-space: pre-line;
            }

            .site-modal-actions {
                display: flex;
                justify-content: flex-end;
                gap: 10px;
                padding: 0 20px 20px;
            }

            .site-modal-button {
                border: 0;
                border-radius: 6px;
                padding: 10px 16px;
                cursor: pointer;
                font-size: 14px;
                font-weight: 700;
            }

            .site-modal-button-secondary {
                border: 1px solid #285E9E;
                background: transparent;
                color: #285E9E;
            }

            .site-modal-button-secondary:hover {
                background: rgba(40, 94, 158, 0.08);
            }

            .site-modal-button-primary {
                background: #68A535;
                color: #ffffff;
            }

            .site-modal-button-primary:hover {
                background: #5ba51e;
            }
        `;
        document.head.appendChild(style);
    }

    function getModal() {
        injectStyles();

        let modal = document.getElementById('site-modal');
        if (modal) {
            return modal;
        }

        modal = document.createElement('div');
        modal.id = 'site-modal';
        modal.className = 'site-modal-backdrop';
        modal.innerHTML = `
            <div class="site-modal-box" role="dialog" aria-modal="true" aria-labelledby="site-modal-title">
                <div class="site-modal-header">
                    <p class="site-modal-brand">
                        <span class="site-modal-brand-green">+Controle</span>
                        <span class="site-modal-brand-blue">-Tempo</span>
                    </p>
                    <h2 id="site-modal-title" class="site-modal-title"></h2>
                </div>
                <p id="site-modal-message" class="site-modal-message"></p>
                <div class="site-modal-actions">
                    <button type="button" id="site-modal-cancel" class="site-modal-button site-modal-button-secondary">Cancelar</button>
                    <button type="button" id="site-modal-confirm" class="site-modal-button site-modal-button-primary">OK</button>
                </div>
            </div>
        `;

        document.body.appendChild(modal);
        return modal;
    }

    function openModal(options) {
        const modal = getModal();
        const title = modal.querySelector('#site-modal-title');
        const message = modal.querySelector('#site-modal-message');
        const cancelButton = modal.querySelector('#site-modal-cancel');
        const confirmButton = modal.querySelector('#site-modal-confirm');

        title.textContent = options.title || 'Atenção';
        message.textContent = options.message || '';
        cancelButton.textContent = options.cancelText || 'Cancelar';
        confirmButton.textContent = options.confirmText || 'OK';
        cancelButton.style.display = options.showCancel ? 'inline-block' : 'none';

        modal.classList.add('is-open');
        confirmButton.focus();

        return new Promise((resolve) => {
            function close(result) {
                modal.classList.remove('is-open');
                confirmButton.removeEventListener('click', confirmHandler);
                cancelButton.removeEventListener('click', cancelHandler);
                modal.removeEventListener('click', backdropHandler);
                document.removeEventListener('keydown', escapeHandler);
                resolve(result);
            }

            function confirmHandler() {
                close(true);
            }

            function cancelHandler() {
                close(false);
            }

            function backdropHandler(event) {
                if (event.target === modal) {
                    close(false);
                }
            }

            function escapeHandler(event) {
                if (event.key === 'Escape') {
                    close(false);
                }
            }

            confirmButton.addEventListener('click', confirmHandler);
            cancelButton.addEventListener('click', cancelHandler);
            modal.addEventListener('click', backdropHandler);
            document.addEventListener('keydown', escapeHandler);
        });
    }

    window.siteAlert = function (message, title) {
        return openModal({
            title: title || 'Atenção',
            message,
            confirmText: 'Entendi',
            showCancel: false
        });
    };

    window.siteConfirm = function (message, title) {
        return openModal({
            title: title || 'Confirmar ação',
            message,
            cancelText: 'Cancelar',
            confirmText: 'Confirmar',
            showCancel: true
        });
    };

    document.addEventListener('click', async function (event) {
        const link = event.target.closest('[data-confirm-message]');
        if (!link) {
            return;
        }

        event.preventDefault();

        const confirmed = await window.siteConfirm(
            link.dataset.confirmMessage,
            link.dataset.confirmTitle || 'Confirmar ação'
        );

        if (confirmed) {
            window.location.href = link.href;
        }
    });
})();
